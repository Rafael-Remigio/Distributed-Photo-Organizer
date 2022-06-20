import socket
import selectors
import os
import socket
import sys
import fcntl

class Client:
    """Chat Client process."""

    def __init__(self, name: str = "CLient"):
        """Initializes chat client."""
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # solve error address already in use error
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sock.setblocking(False)
        self.sel = selectors.DefaultSelector()



    def connect(self,host,port):
        """Connect to chat server and setup stdin flags."""

        self.sock.connect_ex((host,port))
        self.sel.register(self.sock, selectors.EVENT_READ, self.receive)

    def receive(self,conn):
        """receive images"""

    def keyboard_data(self,stdin):

        input = format(stdin.read())
        if input[0:5] == '/list': #/list
            """LIST ALL IMAGES"""
        elif input[0:4] == '/get': #get imageName
            """get image"""
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