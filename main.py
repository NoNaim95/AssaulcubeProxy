#!/usr/bin/python3
import sys
from pyproxy import Proxy
from packethandler import PacketHandler
from packet import Packet
from binascii import unhexlify, hexlify
import time
import os

#sys.stdout = open("/tmp/myfifo","w")
proxy = Proxy("192.168.0.204",int(sys.argv[1]),28763)
proxy.route(packethandler=PacketHandler(proxy))



#loginseqarray = open("./logindbg3","r").read().split("\n")
#for packetdata in loginseqarray:
#    packetdata = unhexlify(packetdata)
#    if packetdata[0] == 0xa0 and False:
#        packetdata = list(packetdata)
#        packetdata[0] = 0xa1
#        packetdata = bytearray(packetdata)
#    print("sending packet",packetdata.hex())
#    proxy.sendPacket(Packet(packetdata,dstaddr=proxy.server))
#    time.sleep(0.05)
