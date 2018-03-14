#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import threading, re

class BlockDomain(threading.Thread):
    def __init__(self, filename=None, debug_mode=False):
        threading.Thread.__init__(self)
        self.filename=filename
        self.debug_mode=debug_mode
        # cache
        self.decisionDicCache={}
        self.domainTableCache=[]
        self.lockcache=threading.Lock()
        self.limitsizeoftable=800 # size of cache entries

        if self.filename:
            self.parseFile()

    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def parseFile(self):
        try:
            with open(self.filename, 'r') as fd:
                for line in fd:
                    line=line.replace('\\','').strip()
                    line=line.replace(' ','') # remove spaces
                    line=re.sub('#.*','', line) # remove comments
                    line=re.sub('http.*://','', line)
                    line=re.sub('/.*','', line) # remove urn
                    line=re.sub('^\.\*','', line) # remove joker
                    line=re.sub('[$*\^\n]', '', line)
                    if line and line not in BlockDomain.blacklist:
                        BlockDomain.blacklist.append(line)
        except:
            print("Impossible to parse file '{}'".format(self.filename))

    def isDomainAllowed(self, domain):
        decision=True # default
        # search in cache
        if domain in self.domainTableCache:
            # search decision in cache
            try:
                decision=self.decisionDicCache[domain]
            except:
                pass

        else: # not in cache
            dom=[x for x in domain.split('.') if x!='']
            for d in BlockDomain.blacklist:
                if domain.endswith(d):
                    d=[x for x in d.split('.') if x!='']
                    count=0
                    for a,b in zip(d[::-1], dom[::-1]):
                        if a==b:
                            count+=1

                    if count==len(d):
                        self.debug("Domain is deny : {}".format(domain))
                        decision=False
                        break
            
            # update cache
            self.lockcache.acquire()
            self.domainTableCache.append(domain)
            self.decisionDicCache[domain]=decision
            # purge cache
            try:
                if len(self.domainTableCache)>self.limitsizeoftable:
                    del self.decisionDicCache[self.domainTableCache[0]]
                    del self.domainTableCache[0] # remove oldest
            except:
                print ("error : impossible to purge ! ")

            self.lockcache.release()

        return decision


BlockDomain.blacklist=[]

if __name__ == "__main__":
    def testDomain(domain, bd):
        print ("{} : {}".format(domain, bd.isDomainAllowed(domain)))

    bd=BlockDomain("../utests/deny_domain.txt", True)
    testDomain( "www.test.fr", bd)
    testDomain( "test.fr", bd)
    testDomain( "qwz.fr", bd)
    testDomain( "test.net", bd)
    testDomain( "fr.test.net", bd)
    testDomain( "fr.test.net", bd)

