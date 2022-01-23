from TeslaBLE import BLE

tesla_ble = BLE("private_key.pem")

print("Scanning for vehicles...")
list = tesla_ble.scan()
# list choices and prompt user to select one
print("Please select a vehicle:")
for i, vehicle in enumerate(list):
    print(f"{i}: {vehicle.name()} [{vehicle.address()}]")
choice = int(input("Enter choice: "))
vehicle = list[choice]

if (vehicle != None):
    print("Connecting to vehicle...")
    vehicle.connect()

    if not vehicle.isConnected():
        print("Vehicle failed to connect")
        exit()

    if not vehicle.isAdded():
        print("Tap your keycard on the center console")
        vehicle.whitelist()

    command = ""
    while True:
        print("Commands available: [EXIT, LOCK, UNLOCK, OPEN_TRUNK]")
        command = input("Enter command: ")
        command = command.upper()
        if command == "LOCK":
            vehicle.lock()
        elif command == "UNLOCK":
            vehicle.unlock()
        elif command == "OPEN_TRUNK":
            vehicle.open_trunk()
        elif command == "EXIT":
            break
        else:
            print("Unknown command")
    vehicle.disconnect()
    print("Vehicle disconnected successfully")
else:
    print("Vehicle not found")
    exit()
