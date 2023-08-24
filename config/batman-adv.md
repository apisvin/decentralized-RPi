# BATMAN-adv

This file summarizes the steps to follow to configure a raspberry pi in a mesh network. 

## 1. install batctl to manage the mesh network : 

	sudo apt-get install -y batctl bridge-utils

## 2. write a shell file that will configure the network interfaces. With the file editor, create ~/start-batman-adv.sh

	nano ~/start-batman-adv.sh

## 3. Copy/paste this inside the file. /!\ Modify IP address for each raspberry pi at the end.

	#! /bin/sh

	# Activate batman-adv
	sudo modprobe batman-adv

	# Disable and configure wlan1
	wpa_cli terminate
	sudo ip link set wlan1 down
	sudo iwconfig wlan1 mode ad-hoc
	sudo iwconfig wlan1 essid camnet 
	sudo iwconfig wlan1 channel 1
	sleep 1s
	sudo ip link set wlan1 up

	#batman interface to use
	sudo batctl if add wlan1
	sudo ifconfig bat0 mtu 1468

	# tell batman this is a gateway client
	sudo batctl gw_mode server

	# Enable ip forwarding
	sudo sysctl -w net.ipv4.ip_forward=1
	# forward ip packet between eth0 and bat0
	sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
	sudo iptables -A FORWARD -i eth0 -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
	sudo iptables -A FORWARD -i bat0 -o eth0 -j ACCEPT
	# forward ip packet between bat0 and wlan0
	sudo iptables -t nat -A POSTROUTING -o bat0 -j MASQUERADE
	sudo iptables -A FORWARD -i bat0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
	sudo iptables -A FORWARD -i wlan0 -o bat0 -j ACCEPT
	sleep 1s

	#activate batman interface 
	sudo ifconfig wlan1 up
	sudo ifconfig bat0 up

	# Fix IPv4 of DHCP server
	sudo ifconfig bat0 192.168.199.x/24 #Change "x" with the number of the Raspberry Pi


The Pi need to act as DHCP server. It needs to know how to assign IPv4 addresses. Install DHCP software : 
	
	sudo apt-get install -y dnsmasq


Configure the DHCP server by editing the dnsmasq.conf file as root user:

	sudo nano /etc/dnsmasq.conf
	
and add this line at the end : 

	interface=bat0
	dhcp-range=192.168.199.2,192.168.199.99,255.255.255.0,12h


 ## 4. This file need to be executed. Make the start-batman-adv.sh file executable with command :

	chmod +x ~/start-batman-adv.sh

## 5. In order to manage the wireless interface, stop the automatic DHCP process to use wlan1 : 

	sudo nano /etc/dhcpcd.conf

Add the following line at the bottom of the file any other added interface lines (like wlan0 if you configured access point).

	denyinterfaces wlan1

## 6. Make sure the startup script gets called by editing file /etc/rc.local as root user, e.g.

	sudo nano /etc/rc.local

and insert:

	/home/pi/start-batman-adv.sh & 


before the last line : exit 0

## 7. reboot the raspberry pi :

	reboot
