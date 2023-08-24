import time
import sys
import select
from aimis.communication.inter.sender import *
from aimis.communication.inter.receiver import *
from aimis.utils.neighbourhood import *
import logging
import psutil
import os
import time
    
class agent_manager:
    
    def __init__(self):
        """
        hardware_manager is a class that manage the creation and suppression of agents on the hardware.
        There is only one hardware_manager per hardware. Threads can communicate with this class to create
        or remove an agent.
        Args : 
            QtoHardwareManager : queue to send messages to this class 
            Qtosendunicast : queue to send messages to sender_unicast
            Qtosendbroadcast : queue to send messages to sender_broadcast
            selforganization : boolean to activate selforganization comportment
        """
        self.agents = {} #dictionnary containing all launcher classes indentified by their hardwareID


    def add(self,agent):
        """
        add the launcher corresponding to the agent to the launchers list
        Args : 
            launcher : launcher class to add to the hardware
        """
        self.agents[agent.neighbourhood.myself.hardwareID] = agent
        
    def delete(self, agent):
        """
        stop all threads of the agent and remove it from the manager
        """
        self.agents[agent.neighbourhood.myself.hardwareID].stop()
        self.agents.pop(agent.neighbourhood.myself.hardwareID)


    def get(self, hardwareID):
        """
        return the launcher class corresponding to the hardwareID
        """
        return self.launchers[hardwareID]
    
    def is_on_hardware(self, hardwareID):
        """
        return a boolean that tell if hardwareID is contained in launchers list
        """
        return hardwareID in self.launchers
    
    def get_dicqueue(self, hardwareID):
        """
        return the dicqueue class of the launcher corresponing to hardwareID
        """
        try:
            return self.launchers[hardwareID].dicqueue
        except:
            return -1
        
    

