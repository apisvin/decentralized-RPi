import socket
import json
from utils.receiver import put_on_queue 
import logging
import netifaces as ni

UDP_IP = ''


class sender:
    
    def __init__(self,agent_manager, Qtosendunicast, Qtosendbroadcast):
        """
        Class sender is used to send messages to other agents. Sockets are used to communicate between hardware.
        Only one sender is launched per hardware to avoid to open several channel

        Args : 
            hardware_manager : the hardware_manager of the hardware
            Qtosendunicast (Queue) : Queue used to receive messages from other threads that want to communicate with specific IP address
            Qtosendbroadcast (Queue) : Queue used to receive messages from other threads that want to communicate all IP addesses
        """
        self.Qtosendunicast = Qtosendunicast
        self.Qtosendbroadcast = Qtosendbroadcast
        self.agent_manager = agent_manager
        
        self.local_ip = ni.ifaddresses('bat0')[ni.AF_INET][0]['addr']
        
    
    def send_unicast(self):
        """
        Send message to specific agent of the destination field.
        If agent is implemented on the same hardware as source agent. It puts directly the messages on the corresponding queue.
        Else it uses socket to send message 
        """
        PORT = 8000
        s_unicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            # Get message to send
            msg = self.Qtosendunicast.get()
            #check if the destination is on the same hardware
            if(self.manager_hardware.is_on_hardware(msg["destination"]["hardwareID"])):
                #put msg directly on his receiver queue
                dicqueue_dest = self.manager_hardware.get_dicqueue(msg["destination"]["hardwareID"])
                put_on_queue(msg, dicqueue_dest)
            #send msg on network
            else:                    
                addr = (msg["destination"]["ip"], PORT)
                msgJson = json.dumps(msg)
                s_unicast.sendto(msgJson.encode(), addr)
                    
                
                    
    
    def send_broadcast(self):
        """
        Send message in broadcast
        It send to all agents implemented on this hardware and on the socket for broadcast 
        """
        PORT = 8001
        s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            # Get message to send
            msg = self.Qtosendbroadcast.get()
            #send to  all agents on same hardware
            for hardwareID, agent in self.agent_manager.agents.items():
                if(hardwareID != msg["source"]["hardwareID"]): #Do not send to itself
                    put_on_queue(msg, launcher.dicqueue) 
            #And send to network
            msgJson = json.dumps(msg)
            addr = ('192.168.199.255', PORT)
            s_broadcast.sendto(msgJson.encode(), addr)
               
    