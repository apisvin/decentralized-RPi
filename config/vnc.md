# VNC

In order to enable VNC viewer to connect to the raspberry pi, you need to uncomment a line to enable the desktop. Open and change /boot/config.txt : 

    sudo nano /boot/config.txt

Uncomment the following line :

    hdmi_force_hotplug=1

