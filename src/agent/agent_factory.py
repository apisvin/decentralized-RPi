from queue import Queue
import threading
import time
import sys
import select
from aimis.communication.inter.sender import *
from aimis.communication.inter.receiver import *
from aimis.utils.neighbourhood import *
from aimis.utils.dicqueue import *
from aimis.agent.agent import Agent
import logging
from multiprocessing import Process



class agent_factory:
    """
    la classe agent_factory cree les classes et 
    lance l ensemble des threads necessaires a la creation d un agent 
    On lui donne en argument toutes les infos de l agent cree et 
    c est lui qui cree dicqueue
    
    """

    def create_agent(agenttype, Qtosendunicast, Qtosendbroadcast) -> Agent:
        """
        Launcher class represents a agent and start all of its threads 
        This class contains all the informatioin relative to the agent.
        Args : 
            agenttype : string specifiing the type of agent
            Qtosendunicast : queue to send messages to sender_unicast
            Qtosendbroadcast : queue to send messages to sender_broadcast
            QtoHardwareManager : queue to send messages to the hardware_manager  
            folder : a folder assigned for the agent. It can either access or safe data in this folder dependeing of its type
            t_b : time from time.time() when the benchmark is launched
        """ 
        myself = neighbour(ip="", agenttype=agenttype) #to know all paramters of myself as neighbour
        myself.generate_own_IP()
        n = neighbourhood(myself) #to store all neighbours
        if agenttype == "detectorONNX":
            from aimis.agent.detectorONNX import detectorONNX
            detector = detectorONNX(n, Qtosendunicast, Qtosendbroadcast)
            threading.Thread(target=detector.launch, name="detectorONNX").start()
            return detector
        if agenttype == "detectorTPU":
            from aimis.agent.detectorTPU import detectorTPU
            detector = detectorTPU(n, Qtosendunicast, Qtosendbroadcast)
            threading.Thread(target=detector.launch, name="detectorTPU").start()
            return detector
        elif agenttype == "tracker":
            from aimis.agent.tracker import tracker
            t = tracker(n, Qtosendunicast, Qtosendbroadcast)
            threading.Thread(target=t.launch, name="tracker").start()
            return t
        elif agenttype == "counter":
            from aimis.agent.counter import Counter
            c = Counter(n, Qtosendunicast, Qtosendbroadcast)
            threading.Thread(target=c.launch, name="counter").start()
            return c
        elif agenttype == "recorder":
            from aimis.agent.recorder import Recorder
            r = Recorder(n, Qtosendunicast, Qtosendbroadcast)
            threading.Thread(target=r.launch, name="recorder").start()
            return r
        else:
            logging.debug("worker name not known...")
        
        