from src.client import Client
import sys


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) <= 0:
        print("insert deamon port")
        sys.exit()
    d = Client("localhost",int(args[0]),args[1])

    d.loop()