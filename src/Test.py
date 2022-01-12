# This file is for testing the other ones

from TeslaController import TeslaVehicle


vehicle = TeslaVehicle("00:00:00:00:00:00", "SOME_NAME")

# private_key = vehicle.getPrivateKey()
# public_key = vehicle.getPublicKey()
# print("Private key: {}".format(private_key))
# print("Public key: {}".format(public_key))

init_msg = vehicle.initMsg()
# print bytes in hex
print("Init message: {}".format(init_msg))

test_msg = vehicle.encrypt_message(init_msg)
print("Test message: {}".format(test_msg))