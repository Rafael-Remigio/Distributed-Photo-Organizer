

from os import listdir
import os
import socket
from os.path import isfile, join
import imagehash
from PIL import Image
import selectors
from daemon import imageHashing


sel = selectors.DefaultSelector()

class daemon:
    """Daemon object"""

    def __init__(self,host: str, port: int,isMaster : bool = False, imagesFolder: str = ""):
                # Server details, host (or ip) to bind to and the port
        self.host = host
        self.port = port
        self.imagesFolder = imagesFolder
        # Events are send back to the given callback

        # Nodes that have established a connection with this node
        self.nodes_inbound = []  # Nodes that are connect with us N->(US)

        # Nodes that this nodes is connected to
        self.nodes_outbound = []  # Nodes that we are connected to (US)->N

        # A list of nodes that should be reconnected to whenever the connection was lost
        self.reconnect_to_nodes = []

        # Create a unique ID for each node if the ID is not given.
        if not isMaster:
            self.port = 5000
            self.id = "master"
        else:
            self.id = str(port) # Make sure the ID is a string!

        # Start the TCP/IP server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()

        self.localImages = imageHashing(imagesFolder)



    
    def init_server(self) -> None:
        """Initialization of the TCP/IP server to receive connections. It binds to the given host and port."""
        print(f"Initialisation of the Node on port: {self.port} on node ({self.id})")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)


    def imageHashing(Folder):
        
        imageHashes = {}  # name : hash

    
        files = [f for f in listdir(Folder) if isfile(join(Folder, f))]
    
    
        for currentImage in files:
            hash = imagehash.average_hash(Image.open(Folder[0] + currentImage))
            if (hash in imageHashes.values()):
                print("Image  "+ (Folder + currentImage)+" is repeated."+ " It was Removed")
                os.remove(Folder + currentImage)
                continue
            print(currentImage + "   " + hash.__str__())
            imageHashes[Folder + currentImage] = hash


        return imageHashes
    
    def loop(self):
        
        sel.register(self.sock, selectors.EVENT_READ, self.accept)