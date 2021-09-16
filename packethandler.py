from binascii import unhexlify, hexlify
import struct
from binascii import hexlify
from packet import Packet
import sys


import parser
from parser import packetuint as pkui, packetint as pki
from assaultcubepacket import INFOLEN, INFOSTART, InfoPacket

class PacketHandler():
    spinb = False
    uni = 0
    lastMSGpacket = b""
    def __init__(self,proxy):
        self.proxy = proxy

    def injectPacket(self,packet):
        self.proxy.sendPacket(packet)

    def hook(self,packet):
        if packet.srcaddr == self.proxy.client:
            if len(packet.data) > 12 and packet.data[INFOSTART] == 3:
                packet = InfoPacket.Packetoverload(packet)
                packet.gamedata.printdata()
                if self.spinb:
                    pass
            if b"ABCDE" in packet.data:
                print(packet.data.hex())
                self.lastMSGpacket = packet.data
            if b"spinbot" in packet.data:
                PacketHandler.spinb = True
            if b"spinbot off" in packet.data:
                PacketHandler.spinb = False

        return packet
