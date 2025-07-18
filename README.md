# PlantTimer

## Purpose
This is a software for tracking when you need to water and care for your plants. It can run as a server, and be viewed remotely on other devices. Either via LAN or WAN connection. Thanks to Python, this program is capable of running on any modern OS, like Windows, MacOS and Linux.

## Screenshots
![Screenshot](https://github.com/HaydenHildreth/PlantTimer/blob/main/assets/preview1.png)
![Screenshot](https://github.com/HaydenHildreth/PlantTimer/blob/main/assets/preview2.png)
![Screenshot](https://github.com/HaydenHildreth/PlantTimer/blob/main/assets/preview3.png)
![Screenshot](https://github.com/HaydenHildreth/PlantTimer/blob/main/assets/preview4.png)

## Dependencies
* Python 3

* Bottle (package)

## Instructions
Have Python 3 and pip installed


Install bottle
```
pip install bottle
```

Clone repository
```
git clone https://github.com/HaydenHildreth/PlantTimer.git
```

Go into folder
```
cd foldername
```

Run python script to launch server
```
python src/main.py
```

Add plants on your new server, at 127.0.0.1:8080

## Network setup
This portion depends how you intend to use the program, and the Operating System which is hosting the service as well.

If you intend to use the program from another network (without VPN), you will need to open the port on your network's router, in addition to opening the ports on your local machine. 

If you intend to use the program from machine's located on the server's network, you will only need to open the ports on your local machine's firewall, and nothing on the router.

### Local Firewall Guide per OS
#### Windows
Upon running program, Windows will do a UAC that will fill in the local machine's firewall rule. If you "No" on the "Allow this app to make changes to your computer", you will need to clear out this rule, and manually put in the port number of the local Windows Defender Firewall.

#### MacOS
Add the port using pfctl via command line:

Open /etc/pf.conf in a text editor.
Add a line like this:

```
# Open port 8080 for TCP on all interfaces
pass in proto tcp from any to any port 8080
```

Save the file.
Load the changes with:
```sudo pfctl -f /etc/pf.conf```


OR


System Preferences > Security & Privacy > Firewall > Advanced. Add a new entry using the `+`.

#### Linux
```
sudo ufw allow 8080
```
