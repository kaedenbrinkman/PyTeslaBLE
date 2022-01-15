# protobuf
import VCSEC_pb2
# cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
# json
import json


class TeslaUUIDs:
    SERVICE_UUID = "00000211-b2d1-43f0-9b88-960cebf8b91e"       # Tesla Vehicle Service
    CHAR_WRITE_UUID = "00000212-b2d1-43f0-9b88-960cebf8b91e"    # To Vehicle
    CHAR_READ_UUID = "00000213-b2d1-43f0-9b88-960cebf8b91e"     # From Vehicle
    CHAR_VERSION_UUID = "00000214-b2d1-43f0-9b88-960cebf8b91e"  # Version Info


class TeslaVehicle:
    def __init__(self, ble_address, name, counter=0, vehicle_eph_public_key=None):
        self.ble_address = ble_address
        self.ble_name = name

        if vehicle_eph_public_key != None:
            curve = ec.SECP256R1()
            self.vehicle_eph_public_key = ec.EllipticCurvePublicKey.from_encoded_point(curve, vehicle_eph_public_key)
        else:
            self.vehicle_eph_public_key = None

        self.generate_keys()
        self.counter = counter

    def __str__(self):
        return "BLE Address: {}, Name: {}".format(self.ble_address, self.ble_name)
    
    def isInitialized(self):
        return self.vehicle_eph_public_key != None

    def getPrivateKey(self):
        private_key_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_key_bytes

    def getPublicKey(self):
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        return public_key_bytes

    def getKeyId(self):
        public_key = self.getPublicKey()

        digest = hashes.Hash(hashes.SHA1())
        digest.update(public_key)
        return digest.finalize()[:4]

    def getSharedKey(self):
        # creates sha1 hasher for creating shared key
        hasher = hashes.Hash(hashes.SHA1())
        # exchange own private key with car's ephemeral key to create an intermediate shared key
        shared_key = self.private_key.exchange(ec.ECDH(), self.vehicle_eph_public_key)
        # intermediate shared key is then inserted into the hasher
        hasher.update(shared_key)
        # and the first 16 bytes of the hash will be our final shared key
        return hasher.finalize()[:16]

    def generate_keys(self):
        # checks for a file named private_key.pem
        # if it exists, load the key
        # else generate a new key
        try:
            with open("private_key.pem", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        except FileNotFoundError:
            # generate a new key
            private_key = ec.generate_private_key(
                ec.SECP256R1(), default_backend())
            # save the key
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open("private_key.pem", 'wb') as pem_out:
                pem_out.write(pem)
            print("Generated private key")
        self.private_key = private_key
        self.public_key = private_key.public_key()

    def signedToMsg(self, message):
        if not self.isInitialized():
            raise Exception('Car\'s ephermeral key not yet loaded!')
        shared_secret = self.getSharedKey()
        encryptor = AESGCM(shared_secret)
        nonce = bytearray()
        nonce.append((self.counter >> 24) & 255)
        nonce.append((self.counter >> 16) & 255)
        nonce.append((self.counter >> 8) & 255)
        nonce.append(self.counter & 255)

        umsg_to = VCSEC_pb2.ToVCSECMessage()
        umsg_to.unsignedMessage.CopyFrom(message)

        encrypted_msg = encryptor.encrypt(
            nonce,
            umsg_to.SerializeToString(),
            None
        )

        msg = VCSEC_pb2.ToVCSECMessage()
        signed_msg = msg.signedMessage
        signed_msg.protobufMessageAsBytes = encrypted_msg[:-16]
        signed_msg.signatureType = VCSEC_pb2.SIGNATURE_TYPE_AES_GCM
        signed_msg.counter = self.counter
        signed_msg.signature = encrypted_msg[-16:]
        signed_msg.keyId = self.getKeyId()

        self.counter += 1
        return self.prependLength(msg.SerializeToString())
    
    def unsignedToMsg(self, message):
        msg = VCSEC_pb2.ToVCSECMessage()
        unsigned_msg = msg.unsignedMessage
        unsigned_msg.CopyFrom(message)
        return self.prependLength(msg.SerializeToString())

    def prependLength(self, message):
        # Extends the length of the byte array by two
        # Shifts all bytes to the right by two
        # Sets the first two bytes to the length of the message
        return bytearray([len(message) >> 8, len(message) & 0xFF]) + message
    
    def loadEphemeralKey(self, key):
        curve = ec.SECP256R1()
        self.vehicle_eph_public_key = ec.EllipticCurvePublicKey.from_encoded_point(curve, key)

    def setCounter(self, counter):
        self.counter = counter


    ###########################       PROCESS RESPONSES       #############################
    # FromVCSECMessage {
    #     commandStatus {
    #         operationStatus: OPERATIONSTATUS_WAIT
    #     }
    # }
    def handle_notify(self, sender, data):
        # remove first two bytes (length)
        data = data[2:]
        msg = VCSEC_pb2.FromVCSECMessage()
        msg.ParseFromString(data)
        print(msg)
        # TODO: check if the message is signed
        # TODO: get command status
        # TODO: do something with the message
        return 0

    ###########################       VEHICLE ACTIONS       #############################

    # These functions generate a message to perform a particular action, such
    # as unlocking the vehicle. The response is in the form of a byte array.
    # Note: It still needs to be encrypted and prepended.

    def whitelistOp(self):
        # request to add a vehicle to the whitelist, request permissions
        msg = VCSEC_pb2.UnsignedMessage()
        whitelist_operation = msg.WhitelistOperation
        permissions_action = whitelist_operation.addKeyToWhitelistAndAddPermissions
        permissions_action.key.PublicKeyRaw = self.getPublicKey()
        permissions = permissions_action.permission
        permissions.append(VCSEC_pb2.WHITELISTKEYPERMISSION_LOCAL_DRIVE)
        permissions.append(VCSEC_pb2.WHITELISTKEYPERMISSION_LOCAL_UNLOCK)
        permissions.append(VCSEC_pb2.WHITELISTKEYPERMISSION_REMOTE_DRIVE)
        permissions.append(VCSEC_pb2.WHITELISTKEYPERMISSION_REMOTE_UNLOCK)
        whitelist_operation.metadataForKey.keyFormFactor = VCSEC_pb2.KEY_FORM_FACTOR_ANDROID_DEVICE

        msg2 = VCSEC_pb2.ToVCSECMessage()
        msg2.signedMessage.signatureType = VCSEC_pb2.SIGNATURE_TYPE_PRESENT_KEY
        msg2.signedMessage.protobufMessageAsBytes = msg.SerializeToString()
        return self.prependLength(msg2.SerializeToString())

    def unlockMsg(self):
        # unlocks the vehicle
        return self.rkeActionMsg(VCSEC_pb2.RKEAction_E.RKE_ACTION_UNLOCK)

    def lockMsg(self):
        return self.rkeActionMsg(VCSEC_pb2.RKEAction_E.RKE_ACTION_LOCK)

    def openTrunkMsg(self):
        # opens the rear trunk
        return self.rkeActionMsg(VCSEC_pb2.RKEAction_E.RKE_ACTION_OPEN_TRUNK)

    def rkeActionMsg(self, action):
        # executes the given RKE action
        msg = VCSEC_pb2.UnsignedMessage()
        msg.RKEAction = action
        return self.signedToMsg(msg)

    def vehiclePublicKeyMsg(self):
        # requests the public key of the vehicle
        msg = VCSEC_pb2.UnsignedMessage()
        info_request = msg.InformationRequest
        info_request.informationRequestType = VCSEC_pb2.INFORMATION_REQUEST_TYPE_GET_EPHEMERAL_PUBLIC_KEY
        key_id = info_request.keyId
        key_id.publicKeySHA1 = self.getKeyId()
        return self.unsignedToMsg(msg)
