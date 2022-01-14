# This file is for testing the other ones

from TeslaController import TeslaVehicle
import VCSEC_pb2


vehicle = TeslaVehicle("00:00:00:00:00:00", "SOME_NAME")

# private_key = vehicle.getPrivateKey()
# public_key = vehicle.getPublicKey()
# print("Private key: {}".format(private_key))
# print("Public key: {}".format(public_key))

# init_msg = vehicle.initMsg()
# print("Init message: {}".format(init_msg))
# test_msg = vehicle.encrypt_message(init_msg)
# print("Test message: {}".format(test_msg))

response = b'\x00\x04\x1a\x02\x18\x02'
print(response)
msg = VCSEC_pb2.FromVCSECMessage()
msg.ParseFromString(bytes(response))
print(msg)