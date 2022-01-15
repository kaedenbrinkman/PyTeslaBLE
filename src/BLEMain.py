# This is the file to run for interacting with vehicles

# Requirement: pip install bleak
# Requirement: pip install cryptography
# Requirement: pip install protobuf

import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import re
from TeslaController import TeslaVehicle, TeslaUUIDs


tesla_vehicles = []


async def scan():
    print("Scanning for Tesla vehicles...")
    async with BleakScanner() as scanner:
        await asyncio.sleep(5.0)
    for d in scanner.discovered_devices:
        name = d.name
        if re.match("^S[a-f\d]{16}[A-F]$", name):
            tesla_vehicles.append(d)


async def run(address, name, nickname, paired=False, public_key=None):
    print("Connecting to {} ({})...".format(name, address))
    if public_key is not None and len(public_key) < 10:
        public_key = None
    vehicle = TeslaVehicle(address, name, 0, public_key)
    try:
        async with BleakClient(address) as client:
            print("Connected")
            # UUIDS: SERVICE_UUID, CHAR_WRITE_UUID, CHAR_READ_UUID, CHAR_VERSION_UUID
            # register notifications for responses from vehicle
            await client.start_notify(TeslaUUIDs.CHAR_READ_UUID, callback=vehicle.handle_notify)
            if not vehicle.isInitialized():
                # whitelist operation
                msg = vehicle.whitelistOp()
                await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, msg, response=True)
                print("Sent whitelist request to vehicle...")
                await asyncio.sleep(1.0)

                # get public key
                msg = vehicle.vehiclePublicKeyMsg()
                await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, msg, response=True)
                print("Sent public key request to vehicle...")
                secs_waited = 0
                while not vehicle.isInitialized():
                    print("Waiting for vehicle to respond...")
                    await asyncio.sleep(1.0)
                    secs_waited += 1
                    if secs_waited > 3:
                        msg = vehicle.vehiclePublicKeyMsg()
                        await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, msg, response=True)
                        secs_waited = 0
                        print("Sent public key request to vehicle...")
                print("Vehicle responded with public key")

            # now we are ready to send commands to the vehicle
            # TODO: Do stuff
            lock_msg = vehicle.lockMsg()
            await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, lock_msg, response=True)
            print("Sent lock message to vehicle...")
            await asyncio.sleep(1.0)
            await client.disconnect()
    except Exception as e:
        print("Error connecting: {}".format(e))
        try_again = input("Start over? (y/n): ")
        if try_again != "y":
            exit()

    print("Done")
    exit()


def main():
    file = open(".tesladata", "r")
    vehicles_found = False
    id = 0
    for line in file:
        arr = line.split()
        if len(arr) >= 4:
            address = arr[2]
            bt_name = arr[1]
            nickname = arr[3]
            if not vehicles_found:
                print("SAVED VEHICLES:")
                print("{}\t{}\t{}\t\t\t{}".format(
                    "ID", "Nickname", "BT Name", "BT Address"))
            print("{}\t{}\t\t{}\t{}".format(id, nickname, bt_name, address))
            id += 1
            vehicles_found = True
        else:
            print(len(arr))
            print("Invalid line: {}".format(line))
    if vehicles_found:
        print(
            "Select a vehicle by ID from the list above, or press enter to scan for new vehicles.")
        selection = input()
        while (True):
            selection = selection.strip()
            selection = selection.replace("\n", "")
            if selection != "" and selection.isdigit():
                # go through each line in the file
                file2 = open(".tesladata", "r")
                for line2 in file2:
                    if line2.startswith(selection):
                        # ID   BT_NAME  BT_ADDR   NICKNAME PUBLIC_KEY
                        address = line2.split()[2]
                        public_key = line2.split()[4]
                        bt_name = line2.split()[1]
                        nickname = line2.split()[3]
                        if public_key == "null":
                            public_key = None
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(
                            run(address, bt_name, nickname, True, public_key))
                        file2.close()
                        break
                file2.close()
                print("Invalid selection. Try again:")
                selection = input()
            elif selection == "":
                vehicles_found = False
                break
    file.close()

    if not vehicles_found:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scan())
        print("Found {} Tesla vehicle(s)".format(len(tesla_vehicles)))
        if len(tesla_vehicles) > 0:
            for i, v in enumerate(tesla_vehicles):
                print("{}: {}".format(i, v))
            choice = int(
                input("Enter the number of the vehicle to connect to: "))
            bt_addr = tesla_vehicles[choice].address
            name = tesla_vehicles[choice].name
            paired = False  # TODO: see if we can actually see whether the vehicle is paired
            nickname = input("Enter a nickname for this vehicle: ")
            # id is # lines in file
            id = str(len(open(".tesladata").readlines()))
            # save the vehicle to .tesladata file
            file = open(".tesladata", "a")
            file.write("{}\t{}\t{}\t{}\t{}\n".format(
                id, name, bt_addr, nickname, "null"))
            file.close()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run(bt_addr, name, paired, nickname))


# Run the program
main()
