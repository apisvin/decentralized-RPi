import time
import json
import uuid
import socket
import logging
import netifaces as ni

class neighbour:
    
    def __init__(self, ip, agenttype, hardwareID=""):
        """
        The neighbor class represents an agent of the network. An agent is defined by :
            - its IP address : UDP socket identifier
            - its type : its predefined task that it must accomplish in the system (detection, tracking, ...)
            - level : the level in which the agent belongs in the tree. Level 0 is the lowest level agent (detection)
            - son age : the time since the last "alive" message was received
            - hardwareID : unique identifier given to the agent when it was created
        Args : 
            ip : IP address of the hardware containing the neighbour
            agenttype : type of the neighbour 
            level : level in which the neighbour is in the hierarchy
            hardwareID : unique uuid identifier for each neighbour 
        """
        self.ip=ip
        self.agenttype = agenttype
        self.age = time.time()
        #if no specified hardwareID, create one
        if(hardwareID==""):
            self.hardwareID = uuid.uuid1().hex #random ID to identify neighbour on hardware 
        else:
            self.hardwareID = hardwareID #if specified, give hardwareID

    @classmethod
    def asdict(cls, dictagent):
        """
        constructor based on a dicionnary
        Args : 
            dictagent : dictionnary containing all the information required to create a neighbour
        """
        newNeighbour = cls(ip = dictagent["ip"], agenttype=dictagent["agenttype"])
        newNeighbour.age = time.time()
        newNeighbour.hardwareID = dictagent["hardwareID"]
        return newNeighbour
        
    
    def generate_own_IP(self):
        """
        Procedure that give the ip address of the hardware to the self.ip variable
        """
        self.ip=ni.ifaddresses('bat0')[ni.AF_INET][0]['addr']

    def update_IP(self, newIP):
        """
        Change ip address of the neighbour by newIP
        Args :
            newIP : new IP address to give to the neighbour
        """
        self.IP = newIP
        
    def update_age(self):
        """
        update the age of the neighbour
        """
        self.age = time.time()
    

