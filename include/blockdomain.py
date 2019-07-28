#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import threading, re

class BlockDomain(threading.Thread):
    def __init__(self, filename_deny=None, filename_allow=None, debug_mode=False):
        threading.Thread.__init__(self)
        self.debug_mode=debug_mode
        # cache
        self.decisionDicCache={}
        self.domainTableCache=[]
        self.lockcache=threading.Lock()
        self.limitsizeoftable=800 # size of cache entries

        if filename_deny:
            self.parseFile(filename_deny, False)

        if filename_allow:
            self.parseFile(filename_allow, True)

        
    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def parseFile(self, filename, allow=False):
        try:
            with open(filename, 'r') as fd:
                for line in fd:
                    line=line.replace('\\','').strip()
                    line=line.replace(' ','') # remove spaces
                    line=re.sub('#.*','', line) # remove comments
                    line=re.sub('http.*://','', line)
                    line=re.sub('/.*','', line) # remove urn
                    line=re.sub('^\.\*','', line) # remove joker
                    line=re.sub('[$*\^\n]', '', line)
                    if line:
                        if not allow and line not in BlockDomain.blacklist:
                            BlockDomain.blacklist.append(line)
                        if allow and line not in BlockDomain.whitelist:
                            BlockDomain.whitelist.append(line)
        except:
            print("Impossible to parse file '{}'".format(filename))

    def domainIsInclude(self, list_domain, domain):
        is_include=False
        dom=[x for x in domain.split('.') if x!='']
        for d in list_domain:
            if domain.endswith(d):
                d_str=d
                d=[x for x in d.split('.') if x!='']
                count=0
                for a,b in zip(d[::-1], dom[::-1]):
                    if a==b:
                        count+=1

                if count==len(d):
                    self.debug("Domain {} is a domain/subdomain of {}".format(domain, d_str))
                    is_include=True
                    break
        return is_include

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
            if self.domainIsInclude(BlockDomain.whitelist, domain):
                self.debug("Domain access is allowed (whitelist) : {}".format(domain))
                decision=True
            elif self.domainIsInclude(BlockDomain.blacklist, domain):
                self.debug("Domain access is denied (blacklist) : {}".format(domain))
                decision=False

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
BlockDomain.whitelist=[]

if __name__ == "__main__":
    def testDomain(domain, bd):
        print ("{} : {}".format(domain, bd.isDomainAllowed(domain)))

    bd=BlockDomain("../utests/deny_domain.txt",\
                   "../utests/allow_domain.txt", True)
    testDomain( "www.test.fr", bd)
    testDomain( "test.fr", bd)
    testDomain( "qwz.fr", bd)
    testDomain( "test.net", bd)
    testDomain( "fr.test.net", bd)
    testDomain( "fr.gtf.com", bd)
    testDomain( "gtf.com", bd)
    testDomain( "abcdef.gtf.com", bd)
    testDomain( "qqqq.abcdef.gtf.com", bd)
    testDomain( "abcdef.qwx.fr", bd)