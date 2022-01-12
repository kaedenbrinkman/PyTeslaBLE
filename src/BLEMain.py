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

async def run(device):
    print("Connecting to {}...".format(device))
    async with BleakClient(device) as client:
        print("Connected")
        vehicle = TeslaVehicle(device.address, device.name)
        # UUIDS: SERVICE_UUID, CHAR_WRITE_UUID, CHAR_READ_UUID, CHAR_VERSION_UUID
        init_msg = vehicle.initMsg()
        msg = vehicle.encrypt_message(init_msg)
        await client.write_gatt_char(TeslaUUIDs.CHAR_WRITE_UUID, msg)
        print("Sent message to vehicle...")
        response = await client.read_gatt_char(TeslaUUIDs.CHAR_READ_UUID)
        print("Received response from vehicle: {}".format(response))
        # TODO: Do stuff



        print("Done")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan())
    print("Found {} Tesla vehicle(s)".format(len(tesla_vehicles)))
    if len(tesla_vehicles) > 0:
        for i, v in enumerate(tesla_vehicles):
            print("{}: {}".format(i, v))
        choice = int(input("Enter the number of the vehicle to connect to: "))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(tesla_vehicles[choice]))

# Run the program
main()