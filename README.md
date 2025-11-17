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