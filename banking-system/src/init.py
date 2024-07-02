# init.py
from NetClient import ZmqClientThread

zmqThread = ZmqClientThread(identity="TeamX")
timeStamp = -1
serverMessage = ""
messageUnprocessed = False
