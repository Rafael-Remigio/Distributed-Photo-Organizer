import sys
from src.daemon import daemon


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) <= 0:
        print("INSERT AN IMAGE FOLDER")
        sys.exit()
    if not (args[1]=='5000'):
        d = daemon("localhost",int(args[1]),int(args[2]),False,str(args[0]))
    else:
        d = daemon("localhost",5000,None,True,str(args[0]))

    d.loop()

     

