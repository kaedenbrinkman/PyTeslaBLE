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


async def run(device, public_key=None):
    print("Connecting to {}...".format(device))
    async with BleakClient(device) as client:
        print("Connected")
        vehicle = TeslaVehicle(device.address, device.name, public_key)
        # UUIDS: SERVICE_UUID, CHAR_WRITE_UUID, CHAR_READ_UUID, CHAR_VERSION_UUID
        msg = vehicle.initMsg()
        await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, msg)
        print("Sent message to vehicle...")
        await client.start_notify(TeslaUUIDs.CHAR_READ_UUID, callback=vehicle.handle_notify)
        # TODO: Do stuff

        print("Done")


def main():
    file = open(".tesladata", "r")
    vehicles_found = False
    for line in file:
        print(line)
        vehicles_found = True
    if vehicles_found:
        print(
            "Select a vehicle from the list above, or press enter to scan for new vehicles.")
        selection = input()
        while (True):
            selection = selection.strip()
            selection = selection.replace("\n", "")
            if selection != "" and selection.isdigit():
                for line in file:
                    if line.startswith(selection + "\t"):
                        # ID   BT_NAME  BT_ADDR   NICKNAME PUBLIC_KEY
                        address = line.split("\t")[2]
                        public_key = line.split("\t")[4]
                        if public_key == "null":
                            public_key = None
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(run(address, public_key))
                        break
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
            nickname = input("Enter a nickname for this vehicle: ")
            # save the vehicle to .tesladata file
            file = open(".tesladata", "a")
            file.write("{}\t{}\t{}\t{}\t{}\n".format(
                len(file.readlines()), name, bt_addr, nickname, "null"))
            file.close()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run(tesla_vehicles[choice]))


# Run the program
main()
