# PN532_UART
## Prerequisites
### pynfc
This library can be installed with:
```
sudo apt install libfreefare0
sudo apt install libfreefare-dev
sudo pip3 install pynfc
```
The documentation can be found here (https://github.com/BarnabyShearer/pynfc). Be aware that you will probably have an error, it is solved in [here](https://github.com/BarnabyShearer/pynfc/issues/2). I recommend doing the modifications explained in the previous link before the error occurs in order to avoid it from the beggining. 

## Running the tests
### With an RFID via UART
First of all, change the import in the first line of Client/main.py for this one:
```
from readers.PN532_UART.ReaderThread import startReader
```

After that, connect the RFID reader on the apropiate pins:

| pn532 | RPi B3          |
|-------|-----------------|
|    5V | 5V (pin 4 or 2) |
|   GND | GND (pin 6)     |
|   TXD | RXD (pin10)     |
|   RXD | TXD (pin 8)     |


Then run:
```
python3 GUI.py
```

### Without an RFID reader
As explained in the [general README.md](../../../README.md), if you just want to test the app without a reader, you can run:
```
python3 GUI.py test
```

## Author
* **Pol Pérez** - [Mefiso](https://github.com/Mefiso)
