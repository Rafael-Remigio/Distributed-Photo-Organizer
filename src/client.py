import base64
from io import BytesIO
import socket
import selectors
import os
import socket
import sys
import fcntl
from PIL import Image

from attr import s
from src.protocol import CDProto, ListImage, Message,RegisterMessage, RequestInfo


class Client:
    """Chat Client process."""

    def __init__(self,host,port, name: str = "CLient"):
        """Initializes chat client."""
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # solve error address already in use error
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sock.setblocking(False)
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.protocol = CDProto()

        self.connect()




    def connect(self):
        """Connect to chat server and setup stdin flags."""
        self.sock.connect_ex((self.host,self.port))
        self.sel.register(self.sock, selectors.EVENT_READ, self.receive)
        print("connected to deamon")
        mensagemRegisto = self.protocol.registerClient(self.name)
        self.protocol.send_msg(self.sock,mensagemRegisto)

    def receive(self,conn):
        mensagem = self.protocol.recv_msg(conn)
        if mensagem.command == "ListImage":
            print("List of Images is")
            for i in mensagem.list:
                print("\t"+i)
        elif mensagem.command == "NotFound":
            print("No such Image")
        elif mensagem.command == "ReceiveImage":
            Image.open(BytesIO(base64.b64decode(str.encode(mensagem.image)))).show()
    def keyboard_data(self,stdin):

        input = format(stdin.read())
        if input[0:5] == '/list': #/list
            """LIST ALL IMAGES"""
            mensagem = self.protocol.imageListing()
            self.protocol.send_msg(self.sock,mensagem)
        elif input[0:4] == '/get': #get imageName
            """get image"""
            mensagem = self.protocol.getImage(input.split(" ")[1].rstrip("\n"))
            self.protocol.send_msg(self.sock,mensagem)

        elif input[0:5] == "/exit":
            sys.exit()
        elif input[0:5] == "/help":
            print("/list \n/get imageName \n/exit")
        else:
            pass

        

    def loop(self):
        """Loop indefinetely."""
        orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

        self.sel.register(sys.stdin, selectors.EVENT_READ, self.keyboard_data)

        while True:
            
            sys.stdout.flush()

            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)