

from ast import Break
from os import listdir
import os
import socket
from os.path import isfile, join
import imagehash
from PIL import Image
import selectors
import time
from src.protocol import CDProto, Message,RegisterMessage


class daemon:
    """Daemon object"""

    def __init__(self,host: str, port: int,connectingNode: int,isMaster : bool = False, imagesFolder: str = ""):
                # Server details, host (or ip) to bind to and the port
        self.host = host
        self.port = port
        self.imagesFolder = imagesFolder
        # Events are send back to the given callback
        self.sel = selectors.DefaultSelector()


        self.isMaster = isMaster
        self.connectingNode = connectingNode
        # Create a unique ID for each node if the ID is not given.
        if isMaster:
            self.port = 5000
            self.id = "master"
        else:
            self.id = str(port) # Make sure the ID is a string!

        # Start the TCP/IP server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()

        # PROTOCOL PARA ENVIO DE MENSAGENS E AFINS
        self.protocol = CDProto()
        self.connections = {}

        # For image Control 
        """"Images have as an Identifier their name. The localImages Dict matches the identifier with their respective imagehash"""
        self.imagesFolder = imagesFolder
        self.localImages = self.imageHashing(imagesFolder)


    
    def init_server(self) -> None:
        """Initialization of the TCP/IP server to receive connections. It binds to the given host and port."""
        print(f"Initialisation of the Node on port: {self.port} on node ({self.id})")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)


    def getList(self,dict):
        list = []
        for key in dict.keys():
            list.append(key)

        return list
    
    def accept(self,sock, mask):
        conn, addr = sock.accept()  # Should be ready
        #print('accepted', conn, 'from', addr)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def SendConnections(self):
        for i in self.connections.values():
            self.protocol.send_msg(i,self.protocol.connectionUpdate(self.getList(self.connections)))

    def read(self,conn, mask):
        mensagem = self.protocol.recv_msg(conn)
        if mensagem.command == "disconected":
            self.sel.unregister(conn)
            #print("Closed  " ,conn)    
            for key, value in self.connections.items():
                if value == conn:
                    del self.connections[key]
                    break
            print(self.connections.keys())
            return
        elif mensagem.command == "register":
            address = (mensagem.host,mensagem.port)
            self.connections[address] = conn
            self.SendConnections()
            print(self.connections.keys())

            return
        elif mensagem.command == "ConnectionUpdate":
            #print(mensagem.connections)
            for i in mensagem.connections:
                if (i[0],i[1]) not in self.connections and (i[0],i[1]) != (self.host,self.port):
                    sock = self.connect(i[0],i[1])
                    self.Register(sock,self.host,self.port)
            print(self.connections.keys())

            return


        

    def imageHashing(self,Folder):
        """"IMAGE HASHING
            Will hash all the images from our local folder using the imagehash library
            """        
        imageHashes = {}  # name : hash

    
        files = [f for f in listdir(Folder) if isfile(join(Folder, f))]
    
    
        for currentImage in files:
            hash = imagehash.average_hash(Image.open(Folder + currentImage))
            if (hash in imageHashes.values()):
                print("Image  "+ (Folder + currentImage)+" is repeated."+ " It was Removed")
                os.remove(Folder + currentImage)
                continue
            #print(currentImage + "   " + hash.__str__())
            imageHashes[currentImage] = hash


        return imageHashes
    
    def loop(self):
        
        if not self.isMaster:
            self.MasterSock = self.connect("localhost",self.connectingNode)
            self.Register(self.MasterSock,self.host,self.port)
            self.connections[("localhost",self.connectingNode)] = self.MasterSock



        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)
        while True:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)



    def Register(self,sock,host,port):
        mensagem = self.protocol.register(host,port)
        self.protocol.send_msg(sock,mensagem)

    # Used for debugging as no purpuse, just like as all
    def sendStr(self,sock: socket,Message):
        sock.sendall(str.encode(Message))

    def connect(self,host,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,port))
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.read)
        return sock
    
