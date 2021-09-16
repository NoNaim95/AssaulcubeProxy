import struct
from packet import Packet
from parser import packetuint as pkui, packetint as pki

INFOSTART = 10
INFOLEN = 9

class Gamedata:
    order = [pki,pki,pkui,pkui,pkui,pkui,pki,pkui]
    def __init__(self,packet,offset):
        self.SV_POS = packet.data[offset+0]
        self.clientnum = packet.data[offset+1]
        if self.SV_POS == 3:
            self.x,self.y,self.z,c = pkui.getcoords(packet.data,offset+2)
            self.yaw, c1 = pkui.get(packet.data,offset+2+c)
            self.pitch, c2 = pki.get(packet.data,offset+2+c+c1)
            g, c3 = pkui.get(packet.data,offset+2+c+c1+c2)

    def printdata(self):
        print(str(self.x)+" "*(9-len(str(self.x)))+"|",end="")
        print(str(self.y)+" "*(9-len(str(self.y)))+"|",end="")
        print(self.z)
        print(self.pitch)
        print(self.yaw)

    def serialize(self):
        b = b""
        i,o = 0,0
        attributes = vars(self)
        for attr in attributes:
            b, c = self.order[i].put(int(attributes[attr])*16,b,o) if (2<=i<=4) else self.order[i].put(int(attributes[attr]),b,o)
            o += c
            i += 1
        return b, i+1

class InfoPacket(Packet):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if len(self.data) > 12:
            self.pkcount = struct.unpack_from("!H",self.data,6)[0]
            self.infolen = self.data[INFOLEN]
            self.info = self.data[INFOSTART:INFOSTART+self.infolen]
            self.gamedata = Gamedata(self,INFOSTART)
    
    @classmethod
    def Packetoverload(cls, packet):
        return cls(packet.data,packet.srcaddr,packet.dstaddr)


    def getNFieldsSize(self,n):
        size = 0
        for i in range(n):
            size += self.gamedata.order[i].get(self.data,INFOSTART+size)[1]
        return size

    def serialize(self):
        i,j,removedsum =0,0,0
        for _ in vars(self.gamedata):
            self.data, removed = self.gamedata.order[i].remove(self.data,INFOSTART)
            removedsum += removed
            i+=1
        self.data = list(self.data)
        for byte in list(self.gamedata.serialize()[0]):
            self.data.insert(INFOSTART+j,byte)
            j+=1
        self.data = bytearray(self.data)
        self.data[INFOLEN] += (j - removedsum)


class ChatMsgPacket(Packet):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.countID = struct.unpack_from("!H",self.data,2)[0]

