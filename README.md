# PyTeslaBLE
Python CLI for connecting to Tesla vehicles directly using the BLE API

## Usage
`pip install pyteslable`

```python
from pyteslable import BLE
tesla_ble = BLE("private_key.pem")

print("Scanning for vehicles...")
list = tesla_ble.scan()
print(list)

# Connect to a specific vehicle by BLE address
vehicle = list.getAddress("05:eb:6d:b7:f7:92")
if not vehicle.isAdded():
  print("Tap your keycard on the center console")
  vehicle.whitelist()
vehicle.unlock()
```

## Cryptography Library Modification
If you have the latest `cryptography` library, you will likely get an error about not supporting 4-bit nonces.
For now, the best solution I have is to simply modify the if statement that produces the error.

## Credits
Huge props to Lex Nastin for putting together some documentation for the Tesla BLE API. Check out the documentation [here](https://teslabtapi.lexnastin.com/).

Also many thanks to Kevin Dewald from Neuralink for the BLE library!
