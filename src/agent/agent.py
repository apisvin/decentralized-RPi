from abc import ABC, abstractmethod
import time
import logging
from queue import Queue
import threading
from aimis.utils.dicqueue import *
from aimis.utils.neighbour import *



class Agent():
    
    def __init__(self, neighbourhood, Qtosendunicast, Qtosendbroadcast):
        # mandatoty variables to start an agent 
        self.neighbourhood = neighbourhood
        self.dicqueue = dicqueue(Qtosendunicast, Qtosendbroadcast) #to store all Queue's (communication between threads)
        self.delay = 1
        self.stop_flag = threading.Event()
        # start threads to look for neighbors
        threading.Thread(target=self.receive_alive, name="receive_alive").start()
        threading.Thread(target=self.send_alive, name="send_alive").start()
        threading.Thread(target=self.check_age,  name="check_age").start()
        

    @abstractmethod
    def launch():
        """
        Perform a loop for the specific task the agent is supposed to do.
        """
        pass
    
    def receive_alive(self):
        """
        Receive alive messages from parent and children. It update the age variable of the source agent in neighbourhood
        """
        while True:
            try:
                received = self.dicqueue.Qtowatcher.get(timeout=self.delay)
                received_neighbour = neighbour.asdict(received["source"])
                self.neighbourhood.refresh_cluster(received_neighbour)
            except Exception as e:
                pass
        logging.debug("receive_alive stopped")
            
    def send_alive(self):
        """
        Send alive message to parent and children in neighbourhood to tell them that this agent is alive 
        """
        while True:
            msg = {"source" : self.neighbourhood.myself.__dict__,
                "destination" : "broadcast",
                "method" : "alive",
                "spec" : ""}
            self.dicqueue.Qtosendbroadcast.put(msg)
            
            time.sleep(self.delay) #wait delay seconds
        logging.debug("send_alive stopped")
            
    def check_age(self):
        """
        check the age variable of parent and childrn in neighbourhood every $delay$ seconds. If the age exceeds 3*$delay$ seconds, the agent is supposed dead and removed from neighbourhood.
        """
        while True:
            #TODO : delete neighbour if exceed time limit 
            self.neighbourhood.check_age(5*self.delay)
            time.sleep(self.delay) #wait 5 seconds
        logging.debug("check_age stopped")
        
    def stop(self):
        """
        set stop flag to True to stop all threads
        """
        self.stop_flag.set()