from TeslaBLE import BLE

tesla_ble = BLE("private_key.pem")

list = tesla_ble.scan()
print(list)
vehicle = list.getName("SaaaaaaaaaaaaaaaaF")

if (vehicle != None):
    vehicle.connect()

    if not vehicle.connected():
        print("Vehicle failed to connect")
        exit()

    if not vehicle.isAdded():
        print("Tap your keycard on the center console")
        vehicle.whitelist()

    vehicle.unlock()
else:
    print("Vehicle not found")
    exit()