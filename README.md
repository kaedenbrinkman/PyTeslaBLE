# PyTeslaBLE
Python CLI for connecting to Tesla vehicles directly using the BLE API

*NOTE: This is very much a work-in-progress. I have not gotten communication to work successfully yet.*


## Usage
1. Run BLEMain.py. A scan will run for 5 seconds looking for nearby vehicles.
2. Select the vehicle you would like to connect to.
3. If not alredy present, a private key will be generated named "private_key.pem"
4. The script will attempt communication with the car.

## Running on Windows
Bleak does not yet support pairing on Windows. This script can detect vehicles, but it can only connect to them if they are already paired. If you are trying to connect and it is timing out, this is probably why.

The solution to this problem is to pre-pair the vehicle using another app. I have built a Windows UWP app that can do this. Let me know if this is something that I should share.

## Credits
Huge props to Lex Nastin for putting together some documentation for the Tesla BLE API. Check out the documentation [here](https://teslabtapi.lexnastin.com/).


## Example
Below is an example of how the program works so far:
```
BLEMain.py
SAVED VEHICLES:
ID      Nickname        BT Name                 BT Address
0       My_Car          Sc6b7ccc84c5b6418B      00:00:5E:00:53:AF
Select a vehicle by ID from the list above, or press enter to scan for new vehicles.
0
Connecting to Sc6b7ccc84c5b6418B (00:00:5E:00:53:AF)...
Connected
authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

commandStatus {
  operationStatus: OPERATIONSTATUS_WAIT
  signedMessageStatus {
  }
}

Sent init message to vehicle...
authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

Sent unlock message to vehicle...
authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

authenticationRequest {
  requestedLevel: AUTHENTICATION_LEVEL_DRIVE
}

Done
```