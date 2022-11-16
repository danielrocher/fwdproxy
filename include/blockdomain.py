#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import threading, re


class Node(object):
    def __init__(self):
        self.dic = {}

    def clear(self):
        self.dic.clear()

    def addDatas(self, data, dic=None):
        if len(data)==0 or type(data)!=list:
            return
        # fist time
        dic=self.dic if dic==None else dic
        key=data.pop()
        if key not in dic:
            dic[key]={}
        if len(data)>0:
            self.addDatas(data, dic[key])
        else:
            # finish
            dic[key]={None : None}

    def isInDic(self, data, dic=None, res=False):
        if len(data)==0 or type(data)!=list:
            return res
        dic=self.dic if dic==None else dic
        key=data.pop()
        if key not in dic:
            return res
        else:
            res=True if None in dic[key] else False
        if len(data)>0:
            res=self.isInDic(data, dic[key], res)
        return res

class Domain(Node):
    def __init__(self):
        super(Domain, self).__init__()
        self.append=self.addDomain # alias

    def splitSubDomain(self, domain):
        return [x for x in domain.split('.') if x!='']

    def addDomain(self, domain):
        self.addDatas(self.splitSubDomain(domain))

    def isSubInDomain(self, sub_domain):
        return self.isInDic(self.splitSubDomain(sub_domain))


class BlockDomain(threading.Thread):
    blocklist=Domain()
    allowlist=Domain()
    # cache
    decisionDicCache={}
    domainTableCache=[]
    def __init__(self, filename_deny=None, filename_allow=None, filter_policy=0, debug_mode=False):
        threading.Thread.__init__(self)
        self.debug_mode=debug_mode
        self.filter_policy=filter_policy
        self.lockcache=threading.Lock()
        self.limitsizeoftable=800 # size of cache entries

        if filename_deny:
            self.parseFile(filename_deny, False)

        if filename_allow:
            self.parseFile(filename_allow, True)


    def debug(self, msg):
        if self.debug_mode:
            print (msg)

    def clearCache(self):
        self.decisionDicCache.clear()
        self.domainTableCache.clear()

    def clear(self):
        self.clearCache()
        self.blocklist.clear()
        self.allowlist.clear()

    def parseFile(self, filename, allow=False):
        try:
            with open(filename, 'r') as fd:
                m1=re.compile(r'[\t\s]*([a-z0-9A-Z\-\_\.]{0,70}\.[a-z0-9A-Z]{2,25})')
                for line in fd:
                    r=m1.match(line)
                    if r :
                        line=r.group(1)
                        if line:
                            if not allow:
                                self.blocklist.addDomain(line)
                            else:
                                self.allowlist.addDomain(line)
                    else:
                        self.debug(f"Ignore domain input (parsing error) : {line.strip()}")
        except:
            print("Impossible to parse file '{}'".format(filename))


    def isInAllowList(self, domain):
        if self.allowlist.isSubInDomain(domain):
            self.debug("Domain access is allowed (allowlist) : {}".format(domain))
            return True, True
        return None, False

    def isInBlockList(self, domain):
        if self.blocklist.isSubInDomain(domain):
            self.debug("Domain access is denied (blocklist) : {}".format(domain))
            return True, False
        return None, False

    def isDomainAllowed(self, domain):
        decision = True if self.filter_policy in (0,1) else False # default policy (not in blocklist or allowlist)
        # search in cache
        if domain in self.domainTableCache:
            # search decision in cache
            try:
                decision=self.decisionDicCache[domain]
            except:
                pass

        else: # not in cache
            # filter policy
            if self.filter_policy in (0,2) :
                func1 = self.isInAllowList
                func2 = self.isInBlockList
            else:
                func1 = self.isInBlockList
                func2 = self.isInAllowList
            found, res=func1(domain)
            if found: decision=res
            else:
                found, res=func2(domain)
                if found: decision=res

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


if __name__ == "__main__":
    def testDomain(domain, bd):
        print ("{} : {}".format(domain, bd.isDomainAllowed(domain)))

    bd=BlockDomain("../utests/block_domain.txt",\
                   "../utests/allow_domain.txt", 0, True)
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
