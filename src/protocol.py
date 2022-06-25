from email import message
import json
from multiprocessing.dummy import connection
from socket import socket
import logging
from datetime import datetime
import time

from click import command

class Message:
    """Message Type."""
    def __init__(self,message):
        self.command = "message"
        self.message = message
        
    def toJSON(self):
       return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)
    
    def __str__(self):
        return self.toJSON()


class RegisterMessage(Message):
    """Message to register username in the server."""
    def __init__(self,host,port):
        self.command = "register"
        self.host = host
        self.port = port

class LostConnectionMessage(Message):
    def __init__(self):
        self.command = "disconected"

class ConnectionUpdateMessage(Message):
    """Message to register username in the server."""
    def __init__(self,connections):
        self.command = "ConnectionUpdate"
        self.connections = connections

class ImageInfo(Message):
    def __init__(self, images):
        self.command = "ImageInfo"
        self.images = str(images)

class RequestInfo(Message):
    def __init__(self):
        self.command = "RequestInfo"

class DeleteOnYourEnd(Message):
    def __init__(self,has):
        self.command = "DeleteImage"
        self.has= has

class CDProto:
    """Computação Distribuida Protocol."""

    @classmethod
    def register(cls, host,port: str) -> RegisterMessage:
        """Creates a RegisterMessage object."""
        message = RegisterMessage(host,port)
        return message
    
    def lostConnection(cls) -> LostConnectionMessage:
        """Creates a RegisterMessage object."""
        message = LostConnectionMessage()
        return message

    def connectionUpdate(cls,connections) -> ConnectionUpdateMessage:
        message = ConnectionUpdateMessage(connections)
        #print(message.toJSON())
        return message

    
    def imageInfo(cls,images) -> ImageInfo:
        """Creates a RegisterMessage object."""
        message = ImageInfo(images)
        return message
    
    def requestInfo(cls) -> RequestInfo:
        message = RequestInfo()
        return message

    def Deleteimages(cls,imagehas) -> DeleteOnYourEnd:
        message = DeleteOnYourEnd(imagehas)
        return message

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        """Sends through a connection a Message object."""
        try:
            head = len(msg.toJSON()).to_bytes(2, 'big') # por causa do Header, idk man
            connection.sendall(head   +   str.encode(msg.toJSON())) 
        except Exception as error: #this is here because i dont wanna clear the dicts, its to much work
            print(error)

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        """Receives through a connection a Message object."""
        head = int.from_bytes(connection.recv(2),'big')
        if (head==0):
            return LostConnectionMessage()
        if head == 0:
            return None
        msg = connection.recv(head).decode('utf-8')
        try:        # for the last test
            jason = json.loads(msg)
            if jason['command'] == "register":
                return RegisterMessage(jason['host'],jason['port'])
            if jason['command'] == "ConnectionUpdate":
                return ConnectionUpdateMessage(jason['connections'])
            if jason['command'] == "ImageInfo":
                return ImageInfo(jason['images'])
            if jason['command'] == "RequestInfo" :
                return RequestInfo()
            if jason['command'] == "DeleteImage" :
                return DeleteOnYourEnd(jason['has'])





        except Exception as error: # there is an error, tbh i dont know how this works
                print(error)
        else:
            return None

