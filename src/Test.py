# This file is for testing the other ones

from TeslaController import TeslaVehicle

vehicle = TeslaVehicle("00:00:00:00:00:00", "SOME_NAME")

msg = vehicle.whitelistOp()
print(msg)

msg = vehicle.vehiclePublicKeyMsg()
print(msg)

msg = vehicle.unlockMsg()
print(msg)