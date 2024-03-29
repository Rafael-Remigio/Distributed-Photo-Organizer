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

class RegisterClient(Message):
    """Message to register username in the server."""
    def __init__(self,name):
        self.command = "registerClient"
        self.name = name

class GetImageList(Message):
    def __init__(self):
        self.command = "GetImageList"

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
    
class ListImage(Message):
    def __init__(self,list):
        self.command = "ListImage"
        self.list = list
class RequestInfo(Message):
    def __init__(self):
        self.command = "RequestInfo"

class DeleteOnYourEnd(Message):
    def __init__(self,has):
        self.command = "DeleteImage"
        self.has= has

class GetImageRequest(Message):
    def __init__(self,name):
        self.command = "GetImageRequest"
        self.imageName = name
class ReceiveImage(Message):
    def __init__(self,imagem):
        self.command = "ReceiveImage"
        self.image = imagem 


class sendToDeamon(Message):
    def __init__(self,name,user):
        self.command = "sendToDeamon"
        self.imagem = name
        self.user = user


class AskforImage(Message):
    def __init__(self,name,user):
        self.command = "AskforImage"
        self.imageName = name
        self.user = user

class notFound(Message):
    def __init__(self):
        self.command = "NotFound"

class keepThis(Message):
    def __init__(self,image,name):
        self.command = "keepThis"
        self.image = image
        self.name = name





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

    def imageListing(cls) -> GetImageList():
        mensagem = GetImageList()
        return mensagem

    def ListOfImages(cls,lista) -> ListImage:
        mensagem = ListImage(lista)
        return mensagem
    def imageInfo(cls,images) -> ImageInfo:
        """Creates a RegisterMessage object."""
        message = ImageInfo(images)
        return message
    
    def getImage(cls,name) -> GetImageRequest:
        message = GetImageRequest(name)
        return message

    def requestInfo(cls) -> RequestInfo:
        message = RequestInfo()
        return message

    def notfound(cls) -> notFound:
        message = notFound()
        return message
    
    def actualImage(cls,imagem) -> ReceiveImage:
        message = ReceiveImage(imagem)
        return message

    def sendtoDeamon(cls,imagem,user) -> sendToDeamon:
        message = sendToDeamon(imagem,user)
        return message


    def Deleteimages(cls,imagehas) -> DeleteOnYourEnd:
        message = DeleteOnYourEnd(imagehas)
        return message

    def registerClient(cls,name) -> DeleteOnYourEnd:
        message = RegisterClient(name)
        return message
    
    def askforImage(cls,name,user) -> AskforImage:
        message = AskforImage(name,user)
        return message
    
    def keepthisImage(cls,image,name) -> keepThis:
        message = keepThis(image,name)
        return message

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        """Sends through a connection a Message object."""
        try:
            head = len(msg.toJSON()).to_bytes(4, 'big') # por causa do Header, idk man
            connection.sendall(head   +   str.encode(msg.toJSON())) 
        except Exception as error: #this is here because i dont wanna clear the dicts, its to much work
            #print(error)
            pass

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        """Receives through a connection a Message object."""
        jmsg = b''

        head = int.from_bytes(connection.recv(4),'big')
        if (head==0):
            return LostConnectionMessage()
        while len(jmsg) < head:
                jmsg += connection.recv(head - len(jmsg))
       
        msg = jmsg.decode('utf-8')

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
            if jason['command'] == "registerClient":
                return RegisterClient(jason['name'])
            if jason['command'] == "GetImageList":
                return GetImageList()
            if jason['command'] == "ListImage":
                return ListImage(list(jason['list']))
            if jason['command'] == "GetImageRequest":
                return GetImageRequest(jason['imageName'])
            if jason['command'] == "NotFound":
                return notFound()
            if jason['command'] == "ReceiveImage":
                return ReceiveImage(jason["image"])
            if jason['command'] == "AskforImage":
                return AskforImage(jason["imageName"],jason["user"])
            if jason['command'] == "sendToDeamon":
                return sendToDeamon(jason["imagem"],jason["user"])
            if jason['command'] == "keepThis":
                return keepThis(jason["image"])





        except Exception as error: # there is an error, tbh i dont know how this works
                #print(error)
                pass
        else:
            return None

