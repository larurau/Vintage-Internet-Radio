# Vintage Internet Radio

A Raspberry Pi internet radio in a vintage radio shell, using only two knobs as input.

Based on [pi-radio](https://github.com/blogmywiki/pi-radio/tree/master).

## Setup

Update Pi
```
sudo apt-get update
```

Install mpd and mpc
```
sudo apt-get install mpc mpd
```

Add radio stations
```
mpc add "https://cast1.torontocast.com:2170/;.mp3"
mpc add "http://usa9.fastcast4u.com/proxy/jamz?mp=/1"
```

Test mpc is working by typing
```
mpc play 1
```
Adjust the volume of your sound device by typing
```
alsamixer
```

## Necessary Libraries

To use 
```
import usb.core
import usb.util
```
Pyusb has to be installed
```
sudo pip3 install pyusb
```