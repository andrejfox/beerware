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
