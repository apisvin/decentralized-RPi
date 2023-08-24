from queue import Queue
import threading
import time
import sys
from utils.sender import *
from utils.receiver import *
from utils.neighbour import *
from utils.neighbourhood import *
import logging
import ipaddress
import netifaces as ni
import cv2

#begin only if bat has an IP
while not ni.AF_INET in ni.ifaddresses('bat0'):
    pass
#begin only if ip address is on right subnetwork with batman-adv
ip = ni.ifaddresses('bat0')[ni.AF_INET][0]['addr']
subnet = "192.168.199.0/24"
while ip not in str(list(ipaddress.ip_network(subnet))):
    ip = ni.ifaddresses('bat0')[ni.AF_INET][0]['addr']




def main():
    #database to have agents on hardware
    agent_manager = agent_manager()

    #Queue to communicate with receiver and sender
    Qtosendunicast, Qtosendbroadcast = Queue(), Queue()

    r = receiver(agent_manager)    
    threading.Thread(target=r.receive_unicast, name="receive_unicast").start()
    threading.Thread(target=r.receive_broadcast, name="receive_broadcast").start()
    
    s = sender(agent_manager, Qtosendunicast, Qtosendbroadcast)
    threading.Thread(target=s.send_unicast, name="send_unicast").start()
    threading.Thread(target=s.send_broadcast, name="send_broadcast").start()

    #START HERE 




if __name__ == "__main__":
    
    main()