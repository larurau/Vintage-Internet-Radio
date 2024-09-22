# Vintage Internet Radio

A Raspberry Pi internet radio in a vintage radio shell, using only two knobs as input.

Based on [pi-radio](https://github.com/blogmywiki/pi-radio/tree/master).

## Setup

### First Steps

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

### Further Configuration

#### Configure ALSA to support multiple audio inputs

To get available devices
```
aplay -l
```
In this case hw:1,0 corresponds to the audio jack.

Edit the configuration
```
nano /etc/asound.conf
```
```
pcm.!default {
    type dmix
    ipc_key 1024
    slave {
       pcm "hw:1,0"
       rate 44100
    }
}

ctl.!default {
    type hw
    card 1
}
```

#### Configure Multiple MPD Instances

Create and edit the files
```
sudo nano /etc/mpd.conf
```
```
sudo nano /etc/mpd2.conf
```

They should look like this, replacing user with the actual user and increasing port number
```
music_directory         "/var/lib/mpd/music"
playlist_directory              "/var/lib/mpd/playlists"
db_file                 "/var/lib/mpd/tag_cache"

state_file                      "/var/lib/mpd/state"
sticker_file                   "/var/lib/mpd/sticker.sql"

user                            "larurau"
bind_to_address                 "localhost"

input {
        plugin "curl"
}

decoder {
        plugin                  "hybrid_dsd"
        enabled                 "no"
}

decoder {
        plugin        "wildmidi"
        enabled       "no"
}

audio_output {
    type            "alsa"
    name            "Headphone Jack"
    device          "hw:1,0"
    mixer_type      "software"
}

filesystem_charset              "UTF-8"

port "6600"
```

The other configurations also need there file location specified. 
The entire changes are like this:
```
port            "6601"
pid_file        "/var/run/mpd2/mpd.pid"
```

These locations need to be created and permissions set

```
sudo mkdir /var/run/mpd2
```

```
sudo chown larurau /var/run/mpd2
```

The user running mpd also needs to be specified
```
sudo nano /lib/systemd/system/mpd.service
```
Add the line for the correct user
```
User=
```

To have the additional MPDs start automatically
```
sudo cp /lib/systemd/system/mpd.service /etc/systemd/system/mpd2.service
```
```
sudo nano /etc/systemd/system/mpd2.service
```
And replace the ExecStart line with and add the lines
```
ExecStart=/usr/bin/mpd --no-daemon /etc/mpd2.conf
```
```
[Service]
ExecStartPre=/bin/mkdir -p /var/run/mpd2
ExecStartPre=/bin/chown larurau:root /var/run/mpd2```
PermissionsStartOnly=true
```
Reload
```
sudo systemctl daemon-reload
```
Enable to run at bootup
```
sudo systemctl enable mpd
```
```
sudo systemctl enable mpd2
```

Some permissions need to be set as well
```
sudo chown larurau:root /etc/mpd2.conf
sudo chmod 644 /etc/mpd2.conf
```
And files need to be created
```
sudo mkdir /var/run/mpd2
sudo chown larurau:root /var/run/mpd2
```

## Necessary Libraries

Confusingly to use 
```
import usb.core
import usb.util
```
Pyusb has to be installed
```
sudo pip3 install pyusb
```