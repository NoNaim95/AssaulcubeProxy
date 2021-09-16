import os
import binascii
import struct
import ctypes

class packetuint:

    @staticmethod
    def put(n,bytes,offset=0):
        n = ctypes.c_int32(n).value
        bytes = list(bytes)
        if n<0 or n >= (1<<21):
            bytes.insert(0+offset,(0x80 | (n&0x7f)))
            bytes.insert(offset+1,(0x80 | ((n >> 7)&0x7f)))
            bytes.insert(offset+2,(0x80 | ((n >> 14)&0x7f)))
            bytes.insert(offset+3,(n >> 21)&0xff)
            bytes = bytearray(bytes)
            return bytes,4
        elif n<(1<<7):
            bytes.insert(offset,n)
            bytes = bytearray(bytes)
            return bytes,1
        elif n < (1<<14):
            bytes.insert(offset,(0x80 | (n & 0x7f)))
            bytes.insert(offset+1,n>>7)
            bytes = bytearray(bytes)
            return bytes,2
        else:
            bytes.insert(offset,(0x80 | (n & 0x7f)))
            bytes.insert(offset+1,(0x80 | ((n>>7) & 0x7f)))
            bytes.insert(offset+2,n>>14)
            bytes = bytearray(bytes)
            return bytes,3

    @staticmethod
    def replace(n,bytes,offset=0):
        bytes = list(bytes)
        bytes, removed = packetuint.remove(bytes,offset)
        bytes = bytearray(bytes)
        bytes,len = packetuint.put(n,bytes,offset)
        return bytes,len,removed

    @staticmethod
    def remove(bytes,offset=0):
        c=0
        for c in range(packetuint.get(bytes,offset)[1]):
            bytes.pop(offset)
        return bytes, c+1

    @staticmethod
    def get(bytes,offset=0):
        i = 1
        n = bytes[0+offset]
        if n & 0x80:
            n += (bytes[1+offset] << 7) - 0x80
            i=2
            if n & (1<<14):
                n += (bytes[2+offset] << 14) - (1<<14)
                i=3
            if n & (1<<21):
                n += (bytes[3+offset] << 21) - (1<<21)
                i=4
            if n & (1<<28):
                n |= 0xF0000000
        return n,i

    @staticmethod
    def getcoord(bytes,offset=0):
        coord, i = packetuint.get(bytes,offset)
        return ctypes.c_int32(coord).value/16,i

    @staticmethod
    def getcoords(bytes,offset=0):
        x,ix = packetuint.getcoord(bytes,offset)
        y,iy = packetuint.getcoord(bytes,offset+ix)
        z,iz = packetuint.getcoord(bytes,offset+ix+iy)
        return (x,y,z,ix+iy+iz)








class packetint:
    @staticmethod
    def remove(bytes,offset=0):
        bytes = list(bytes)
        c=0
        for c in range(packetint.get(bytes,offset)[1]):
            bytes.pop(offset)
        bytes = bytearray(bytes)
        return bytes, c+1

    @staticmethod
    def replace(n,bytes,offset=0):
        bytes = list(bytes)
        bytes, removed = packetint.remove(bytes,offset)
        bytes = bytearray(bytes)
        bytes,len = packetint.put(n,bytes,offset)
        return bytes,len,removed
        


    @staticmethod
    def put(n,bytes,offset=0):
        n = ctypes.c_int32(n).value
        bytes = list(bytes)
        if n <128 and n > -127:
            bytes.insert(0+offset,n & 0xff)
            bytes = bytearray(bytes)
            return bytes,1
        elif n<0x8000 and n>=-0x8000:
            bytes.insert(0+offset,0x80)
            bytes.insert(1+offset,n & 0xff)
            bytes.insert(2+offset,n>>8 & 0xff)
            bytes = bytearray(bytes)
            return bytes, 3
        else:
            bytes.insert(0+offset,0x81)
            bytes.insert(1+offset,n & 0xff)
            bytes.insert(2+offset,n>>8 & 0xff)
            bytes.insert(3+offset,n>>16 & 0xff)
            bytes.insert(4+offset,n>>24 & 0xff)
            bytes = bytearray(bytes)
            return bytes, 5


    @staticmethod
    def get(bytes,offset=0):
        c = bytes[0+offset]
        i = 1
        if c == 0x80:
            n = bytes[1+offset]
            n |= bytes[2+offset] << 8
            i = 3
            return ctypes.c_short(n).value
        elif c == 0x81:
            n = bytes[1+offset]
            n = bytes[2+offset]<<8
            n = bytes[3+offset]<<16
            n = bytes[4+offset]<<24
            i = 5
            return ctypes.c_int32(n).value
        else:
            return struct.unpack("b",c.to_bytes(1,'little'))[0],i

