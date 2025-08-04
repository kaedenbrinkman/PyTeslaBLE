# PyTeslaBLE
Python library for communicating with Tesla vehicles directly using the BLE API

Note: Tesla has now published an official SDK here: https://github.com/teslamotors/vehicle-command/

:bangbang: | WARNING: This library is not supported by Tesla, and it could break at any moment. It should be noted that this library stores private keys and other sensitive data unencrypted on your machine. I am not responsible for any (extremely unlikely) damage done to your car.
:---: | :---

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
vehicle.connect()
if not vehicle.isAdded():
  print("Tap your keycard on the center console")
  vehicle.whitelist()
# Now we are ready to send commands!
vehicle.unlock()
```

## Cryptography Library Modification
If you have the latest `cryptography` library, you will likely get an error about not supporting 4-bit nonces.
For now, the best solution I have is to simply modify the if statement that produces the error.

## Credits
Huge props to Lex Nastin for putting together some documentation for the Tesla BLE API. Check out the documentation [here](https://teslabtapi.lexnastin.com/).

Also many thanks to Kevin Dewald from Neuralink for the [BLE library](https://github.com/OpenBluetoothToolbox/SimpleBLE)!

-------

(The MIT License)

Copyright (c) 2021-2023 Kaeden Brinkman &lt;kaeden@kaedenb.org&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
