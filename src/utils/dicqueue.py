from queue import Queue
import logging

class dicqueue:

    def __init__(self, Qtosendunicast, Qtosendbroadcast):
        """
        This class is used as a dictionnary of all needed queues for the inter thread communication.
        Indeed, in a multi threading environment, the synchronization is necessary. 
        Queues are data structures to exchange information across multiple threads safely.
        Three queues are common to all agents : Qtosendunicast, Qtosendbroadcast, QtoHardwareManager. 
        The others are created unique to an agent.

        Args : 
            Qtosendunicast (Queue) : a queue used by the unicast sender thread 
            Qtosendbroadcast (Queue) : a queue used by the broadcast sender thread 
            QtoHardwareManager (Queue) : a queue used by the hardware manager
        """
        self.Qtosendunicast =       Qtosendunicast
        self.Qtosendbroadcast =     Qtosendbroadcast
        self.Qtowatcher =           Queue()
