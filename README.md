# PyTeslaBLE
Python CLI for connecting to Tesla vehicles directly using the BLE API

*NOTE: This is very much a work-in-progress. I have not gotten communication to work successfully yet.*


## Usage
1. Run BLEMain.py. A scan will run for 5 seconds looking for nearby vehicles.
2. Select the vehicle you would like to connect to.
3. If not alredy present, a private key will be generated named "private_key.pem"
4. The script will attempt communication with the car.

## Running on Windows
Bleak does not yet support pairing on Windows. This script can detect vehicles, but it can only connect to them if they are already paired.

The solution to this problem is to pre-pair the vehicle using another app. I have built a Windows UWP app that can do this.

## Credits
Huge props to Lex Nastin for putting together some documentation for the Tesla BLE API. Check out the documentation [here](https://teslabtapi.lexnastin.com/).