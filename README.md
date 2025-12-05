(gpio 4)
Sensor0: 'db5a7d0a6461'

(gpio 17)
Sensor1: '8490710a6461'

1. Clone repo in to `~/`
```sh
cd ~
git clone https://github.com/andrejfox/beerware.git
```
---
2. Enable auto start
```sh
mkdir -p ~/.config/systemd/user
cp ~/beerware/startup/beerware.service ~/.config/systemd/user

# remember to rename the user in the absolute paths
# in the .service file (default is admin)
nano ~/.config/systemd/user/beerware.service

systemctl --user daemon-reload
systemctl --user enable beerware.service
systemctl --user start beerware.service
```
---
3. Optionally fix 1024x600 resolution glitching by adding to `/boot/firmware/config.txt`
```sh
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1024 600 60 6 0 0 0
hdmi_force_hotplug=1
disable_overscan=1
```
4. For w1protocol to work do:
```shell
sudo nano /boot/firmware/config.txt
```
```
dtoverlay=w1-gpio,gpiopin=4
dtoverlay=w1-gpio,gpiopin=17,slave=0
```
