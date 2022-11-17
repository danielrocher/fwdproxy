#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import struct

class TLSHelloParser():
    def __init__(self, debug_mode=False):
        self.currindex=0
        self.raw=None
        self.server_name=None
        self.tls_version=None
        self.debug_mode=debug_mode

    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def getHostname(self):
        return self.server_name

    def getTLSVersion(self):
        return self.tls_version
        
    def parseClientHelloHanshake(self, raw):
        self.debug("TLSHelloParser.parseClientHelloHanshake()")
        self.raw=raw
        self.currindex=0
        self.server_name=None
        contenttype= self.getShort()
        if contenttype==0x16: # handshake
            versionTLS= self.getInt()
            if versionTLS>=0x301:
                # self.debug ("Version TLS : 0x{:04X}".format(versionTLS))
                length= self.getInt()
                self.debug ("Lenght {}".format(length))
                handshaketype= self.getShort()
                self.debug ("Handshake type : {}".format(handshaketype))
                if handshaketype==1:
                    self.debug("client hello")
                    self.currindex+=1
                    length= self.getInt()
                    self.debug ("Lenght {}".format(length))
                    versionTLS=self.getInt()
                    self.tls_version=versionTLS
                    if versionTLS>=0x301:
                        self.debug ("Version TLS : 0x{:04X}".format(versionTLS))
                        # Random 32 bytes
                        self.currindex+=32
                        sessionid_length=self.getShort()
                        self.incCurrentindex(sessionid_length)
                        ciphersuite_length=self.getInt()
                        self.incCurrentindex(ciphersuite_length)
                        compression_length=self.getShort()
                        self.incCurrentindex(compression_length)
                        self.getInt() # extensions_length
                        while 1:
                            extension_type=self.getInt()
                            extension_len=self.getInt()

                            if (extension_type==None or extension_len==None):
                                break
                            else:
                                # self.debug ("extension_type : 0x{:04X}".format(extension_type))
                                # self.debug ("extension_len : {}".format(extension_len))
                                if extension_type==0x00: # server_name
                                    self.parseServerNameIndication()
                                    if self.server_name:
                                        return
                                else:
                                    self.getRaw(extension_len)

    def decode(self, data):
        try:
            return data.decode("ascii")
        except:
            pass
        try:
            return data.decode("latin-1")
        except:
            pass
        try:
            return data.decode("utf-8")
        except:
            return None

    def parseServerNameIndication(self):
        self.getInt() # server_name_list_len
        server_name_type=self.getShort()
        if server_name_type==0x00: # host_name
            server_name_len=self.getInt()
            server_name=self.getRaw(server_name_len)
            if len(server_name)==server_name_len:
                self.server_name=self.decode(server_name)
                self.debug ("Hostname : {}".format(self.server_name))


    def getRaw(self, l):
        r=None
        try:
            r=self.raw[self.currindex:self.currindex+l]
            if len(r)<l: return None
        except:
            pass
        self.incCurrentindex(l)
        return r

    def getShort(self):
        r=None
        try:
            r= self.raw[self.currindex]
        except:
            pass
        self.currindex+=1
        return r

    def getInt(self):
        r=None
        try:
            r=struct.unpack('>h', self.raw[self.currindex:self.currindex+2])[0]
        except:
            pass
        self.currindex+=2
        return r

    def incCurrentindex(self, offset):
        try:
            self.currindex+=offset
        except:
            pass


if __name__ == "__main__":
    by = b'\x16\x03\x01\x01\x09\x01\x00\x01\x05\x03\x03\x5a\x98\xfd\xff\xa9\x02\xb5\x2a\x7e\xcc\xe0\xee\x89\xb1\xc5\xc1\x55\xae\x0a\x39\x1d\x67\xf6\xa3\xda\xf5\x45\x36\xb4\x4d\xad\x76\x00\x00\x6c\xc0\x2b\xc0\x2c\xc0\x86\xc0\x87\xc0\x09\xc0\x23\xc0\x0a\xc0\x24\xc0\x72\xc0\x73\xc0\xac\xc0\xad\xc0\x08\xc0\x2f\xc0\x30\xc0\x8a\xc0\x8b\xc0\x13\xc0\x27\xc0\x14\xc0\x28\xc0\x76\xc0\x77\xc0\x12\x00\x9c\x00\x9d\xc0\x7a\xc0\x7b\x00\x2f\x00\x3c\x00\x35\x00\x3d\x00\x41\x00\xba\x00\x84\x00\xc0\xc0\x9c\xc0\x9d\x00\x0a\x00\x9e\x00\x9f\xc0\x7c\xc0\x7d\x00\x33\x00\x67\x00\x39\x00\x6b\x00\x45\x00\xbe\x00\x88\x00\xc4\xc0\x9e\xc0\x9f\x00\x16\x01\x00\x00\x70\x00\x17\x00\x00\x00\x16\x00\x00\x00\x05\x00\x05\x01\x00\x00\x00\x00\x00\x00\x00\x13\x00\x11\x00\x00\x0e\x77\x77\x77\x2e\x72\x65\x73\x79\x64\x65\x76\x2e\x66\x72\xff\x01\x00\x01\x00\x00\x23\x00\x00\x00\x0a\x00\x0c\x00\x0a\x00\x17\x00\x18\x00\x19\x00\x15\x00\x13\x00\x0b\x00\x02\x01\x00\x00\x0d\x00\x16\x00\x14\x04\x01\x04\x03\x05\x01\x05\x03\x06\x01\x06\x03\x03\x01\x03\x03\x02\x01\x02\x03\x00\x10\x00\x0b\x00\x09\x08\x68\x74\x74\x70\x2f\x31\x2e\x31'

    parser=TLSHelloParser(True)
    parser.parseClientHelloHanshake(by)
    parser.getHostname()

