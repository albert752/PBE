# PBE Telemàtica

This is my PBE progect for my Telecomunications Engeneering degree. Use this code wisely!

## Disclaimer for other students
Be aware that this project has been licenced under the MIT licence. Although you are free to use it in whatever way you want, you __MUST__ acknowledge me as the original author. So if you use it for your progect you will have to do so.

## Getting Started

You might have to clone this repo in orther to use the program. Just run:

```
sudo apt update
sudo apt install git -y
git clone https://github.com/albert752/PBE.git
```
And.. thats it! Enjoy!

### Prerequisites
#### Python3
```
sudo apt install python3
```

#### py532lib
It can be found here https://github.com/HubCityLabs/py532lib. In order
for the progect to work, it must have the library on the same directory
so be sure that the folders _quick2wire_ and _py532lib_ are there. To do
so, run inside the RFID directory the following command:
```
git clone https://github.com/HubCityLabs/py532lib.git
```

#### RFID Reader and RPi
Just get the reader on eBay for cheap and whatever recent model of the Raspberry Pi 3.


## Running the tests
### With an RFID reader
First of all, connect the RFID reader on the apropiate pins. Here there
is a small table:

| pn532 | RPi B3          |
|-------|-----------------|
|    5V | 5V (pin 4 or 2) |
|   GND | GND (pin 6)     |
|   SDA | SDA0 (pin3)     |
|   SCL | SCL0 (pin5)     |

Then run:

```
python3 GUI.py
```

### Without an RFID reader
If your purpose is just to test the app without a reader, ypu can do so
by running this command:
```
python3 GUI.py test
```
It will automatically yield the same UID every 3s.

## Licence
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

