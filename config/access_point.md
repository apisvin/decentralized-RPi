# Access point 

This file summarizes the steps to follow to configure a raspberry pi as an access point. Doing so, any device can connect to the network to have real time data.
https://raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/168-raspberry-pi-hotspot-access-point-dhcpcd-method
## 0. OS up to date 

Make sure the raspberry pi up to date : 

	sudo apt update
	sudo apt upgrade

## 1. Wifi dongle configuration

Plug the TL-WN823N wifi dongle in the Pi's USB port. Now, install the driver to use this dongle following instruction in 
https://github.com/Mange/rtl8192eu-linux-driver

Note : if OS is 64 bits, don't change Makefile.


## 2. Raspberry Pi configuration

Install hostapd and dnsmasq :

	sudo apt install hostapd
	sudo apt install dnsmasq

Stop the programmes to configure Raspberry pi : 

	sudo systemctl stop hostapd
	sudo systemctl stop dnsmasq

### Hostapd configuration

Edit hostapd configuration file with :

	sudo nano /etc/hostapd/hostapd.conf

Write the following into the file : 

	interface=wlan0
	driver=nl80211
	ssid=decentralizedRPiAP
	hw_mode=g
	channel=6
	wmm_enabled=0
	macaddr_acl=0
	auth_algs=1
	ignore_broadcast_ssid=0
	wpa=2
	wpa_passphrase=1234567890
	wpa_key_mgmt=WPA-PSK
	rsn_pairwise=CCMP

Note that the name of the access point is decentralizedRPiAP while the password is 1234567890.

To start hostapd at reboot time, type the following in the terminal : 

	sudo systemctl unmask hostapd
	sudo systemctl enable hostapd

To tell hostapd what change it needs to take into account, modify hostapd file : 

	sudo nano /etc/default/hostapd

Modifiy the file to have : 

	DAEMON_CONF="/etc/hostapd/hostapd.conf"


### Dnsmasq configuration

Open the dnsmasq.conf file with

	sudo nano /etc/dnsmasq.conf

At the bottom of the file, add the following :

	interface=wlan0
	domain-needed
	bogus-priv
	dhcp-range=192.168.50.150,192.168.50.200,255.255.255.0,12h


### Interface configuration

The interfaces file is not required and should be empty of any network config. 

	sudo nano /etc/network/interfaces

If the file contains any uncommented line, make a backup : 

	sudo cp /etc/network/interfaces /etc/network/interfaces-backup

And comment all lines in /etc/network/interfaces.


### DHCPCD configuration

Open dhcpcd.conf : 

	sudo nano /etc/dhcpcd.conf

And add at the bottom (under wlan1 configuration if you configured batman-adv) : 

	interface wlan0
	nohook wpa_supplicant
	static ip_address=192.168.50.10/24
	static routers=192.168.50.1

### Test the access point 

You can reboot the raspberry pi and see if "camnetAccessPoint" is available in your available wifi.

