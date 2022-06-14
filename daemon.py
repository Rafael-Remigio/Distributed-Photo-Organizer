import sys
from os import listdir
from os.path import isfile, join
import imagehash
from PIL import Image
import os


def imageHashing(args):

    imageHashes = {}  # name : hash

    if len(args) <= 0:
        print("INSERT AN IMAGE FOLDER")
        sys.exit()


    files = [f for f in listdir(args[0]) if isfile(join(args[0], f))]


    for currentImage in files:
        hash = imagehash.average_hash(Image.open(args[0] + currentImage))
        if (hash in imageHashes.values()):
            print("Image  "+ (args[0] + currentImage)+" is repeated."+ " It was Removed")
            os.remove(args[0] + currentImage)
            continue
        print(currentImage + "   " + hash.__str__())
        imageHashes[currentImage] = hash

    


if __name__ == "__main__":
    args = sys.argv[1:]

    imageHashing(args)
     
     

