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
        print("Enter a command, or 'help' for a list of commands. Type 'exit' to quit.")
        command = input("Enter command: ")
        command = command.upper().replace(' ', '_')
        if command == "LOCK":
            vehicle.lock()
        elif command == "UNLOCK":
            vehicle.unlock()
        elif command == "OPEN_TRUNK":
            vehicle.open_trunk()
        elif command == "OPEN_FRUNK":
            vehicle.open_frunk()
        elif command == "OPEN_CHARGE_PORT":
            vehicle.open_charge_port()
        elif command == "CLOSE_CHARGE_PORT":
            vehicle.close_charge_port()
        elif command == "REMOTE_DRIVE":
            vehicle.remote_drive()
        elif command == "EXIT":
            break
        elif command == "HELP":
            print("\n\n\nCommands available:")
            print("\tEXIT: Exit the program")
            print("\tHELP: Print this message")
            print("\tLOCK: Lock the vehicle")
            print("\tUNLOCK: Unlock the vehicle")
            print("\tOPEN_TRUNK: Open the vehicle's trunk")
            print("\tOPEN_FRUNK: Open the vehicle's front trunk")
            print("\tOPEN_CHARGE_PORT: Open and unlock the vehicle's charge port")
            print("\tCLOSE_CHARGE_PORT: Close and lock the vehicle's charge port")
            print("\tREMOTE_DRIVE: Enable keyless driving")
            print("\n\n")
        else:
            print("Unknown command")
    vehicle.disconnect()
    print("Vehicle disconnected successfully")
else:
    print("Vehicle not found")
    exit()
