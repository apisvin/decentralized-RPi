import socket
import json
import logging
import netifaces as ni
UDP_IP = ''


class receiver():
    
    def __init__(self, agent_manager):
        """
        Class receiver is used to receive messages from other hardware. Sockets are used to communicate between hardware.
        Only one receiver is launched per hardware to avoid to open several channel

        Args : 
            hardware_manager : the hardware_manager of the hardware
            
        """
        self.agent_manager = agent_manager #ATTENTION a cause du passage par multiprocessing cette variable peut ne plus etre actualiser
        self.local_ip = ni.ifaddresses('bat0')[ni.AF_INET][0]['addr']
        
    def receive_broadcast(self):
        """
        Listen the opened socket for broadcasted messages.
        """
        PORT = 8001
        #create socket in broadcast
        s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s_broadcast.bind((UDP_IP,PORT))
        #begin loop
        while True:
            msgReceived, address = s_broadcast.recvfrom(1024)
            msgReceived = msgReceived.decode()
            if(self.local_ip != address[0]): #message not from me
                dictReceived = json.loads(msgReceived)
                for hardwareID, agent in self.agent_manager.agents.items():
                    put_on_queue(dictReceived, agent.dicqueue)
            

    def receive_unicast(self):
        """
        Listen the opened socket for unicasted messages. 
        """
        PORT = 8000
        #create socket in unicast
        s_unicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_unicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_unicast.bind((UDP_IP,PORT))
        while(True):
            msgReceived, address = s_unicast.recvfrom(8192)
            msgReceived = msgReceived.decode()
            if(self.local_ip != address[0]): #message not from me
                dictReceived = json.loads(msgReceived)
                #chercher la bonne dicqueue dans manager_hardware
                dicqueue = self.hardware_manager.get_dicqueue(dictReceived["destination"]["hardwareID"])
                if(dicqueue==-1):
                    logging.warning("message received (destination is not on hardware) : {}".format(dictReceived))
                else:
                    put_on_queue(dictReceived, dicqueue)
                

def put_on_queue(dictReceived, dicqueue):
    """
    Process the message and put it on the correct queue of the dicqueue in function of the method field
    Args : 
        dictReceived : the received dictionnary to put on the right queue
        dicqueue : dicqueue class containing all queues
    """
    if(dictReceived["method"] == "alive"):
        dicqueue.Qtowatcher.put(dictReceived)

