#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018


import unittest, os, time
from include.tlshelloparser import *
from include.blockdomain import *
from include.logs import *

def setUpModule():
    pass
    
def tearDownModule():
    pass

class TLSHelloParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pattern_withtls_1_0(self):
        by = b'\x16\x03\x01\x00\xd7\x01\x00\x00\xd3\x03\x01\xbd\xb8\x33\x54\x1d\x56\x79\x7f\x7e\xbe\x88\x12\xd3\xbd\x3e\x94\x06\x02\x28\x9b\x8c\x96\xdb\xdb\xc7\x90\xbd\xdc\xe0\x0b\xc5\xf8\x00\x00\x62\xc0\x14\xc0\x0a\x00\x39\x00\x38\x00\x37\x00\x36\x00\x88\x00\x87\x00\x86\x00\x85\xc0\x0f\xc0\x05\x00\x35\x00\x84\xc0\x13\xc0\x09\x00\x33\x00\x32\x00\x31\x00\x30\x00\x9a\x00\x99\x00\x98\x00\x97\x00\x45\x00\x44\x00\x43\x00\x42\xc0\x0e\xc0\x04\x00\x2f\x00\x96\x00\x41\xc0\x11\xc0\x07\xc0\x0c\xc0\x02\x00\x05\x00\x04\xc0\x12\xc0\x08\x00\x16\x00\x13\x00\x10\x00\x0d\xc0\x0d\xc0\x03\x00\x0a\x00\xff\x01\x00\x00\x48\x00\x00\x00\x13\x00\x11\x00\x00\x0e\x77\x77\x77\x2e\x72\x65\x73\x79\x64\x65\x76\x2e\x66\x72\x00\x0b\x00\x04\x03\x00\x01\x02\x00\x0a\x00\x1c\x00\x1a\x00\x17\x00\x19\x00\x1c\x00\x1b\x00\x18\x00\x1a\x00\x16\x00\x0e\x00\x0d\x00\x0b\x00\x0c\x00\x09\x00\x0a\x00\x23\x00\x00\x00\x0f\x00\x01\x01'

        parser=TLSHelloParser()
        parser.parseClientHelloHanshake(by)
        self.assertEqual(parser.getTLSVersion(), 0x301)
        self.assertEqual(parser.getHostname(), "www.resydev.fr")


    def test_pattern_withtls_1_1(self):
        by = b'\x16\x03\x01\x00\xd7\x01\x00\x00\xd3\x03\x02\x50\xb3\xdb\x62\xfc\x69\x2f\x98\x83\xdf\x6b\x7c\x05\x94\x5b\xf3\x06\xf0\xcc\xb2\x63\x36\xa3\xd5\x51\x2b\x3e\x45\x80\xc2\x93\x73\x00\x00\x62\xc0\x14\xc0\x0a\x00\x39\x00\x38\x00\x37\x00\x36\x00\x88\x00\x87\x00\x86\x00\x85\xc0\x0f\xc0\x05\x00\x35\x00\x84\xc0\x13\xc0\x09\x00\x33\x00\x32\x00\x31\x00\x30\x00\x9a\x00\x99\x00\x98\x00\x97\x00\x45\x00\x44\x00\x43\x00\x42\xc0\x0e\xc0\x04\x00\x2f\x00\x96\x00\x41\xc0\x11\xc0\x07\xc0\x0c\xc0\x02\x00\x05\x00\x04\xc0\x12\xc0\x08\x00\x16\x00\x13\x00\x10\x00\x0d\xc0\x0d\xc0\x03\x00\x0a\x00\xff\x01\x00\x00\x48\x00\x00\x00\x13\x00\x11\x00\x00\x0e\x77\x77\x77\x2e\x72\x65\x73\x79\x64\x65\x76\x2e\x66\x72\x00\x0b\x00\x04\x03\x00\x01\x02\x00\x0a\x00\x1c\x00\x1a\x00\x17\x00\x19\x00\x1c\x00\x1b\x00\x18\x00\x1a\x00\x16\x00\x0e\x00\x0d\x00\x0b\x00\x0c\x00\x09\x00\x0a\x00\x23\x00\x00\x00\x0f\x00\x01\x01'

        parser=TLSHelloParser()
        parser.parseClientHelloHanshake(by)
        self.assertEqual(parser.getTLSVersion(), 0x302)
        self.assertEqual(parser.getHostname(), "www.resydev.fr")


    def test_pattern_withtls_1_2(self):
        by = b'\x16\x03\x01\x01\x09\x01\x00\x01\x05\x03\x03\x5a\x98\xfd\xff\xa9\x02\xb5\x2a\x7e\xcc\xe0\xee\x89\xb1\xc5\xc1\x55\xae\x0a\x39\x1d\x67\xf6\xa3\xda\xf5\x45\x36\xb4\x4d\xad\x76\x00\x00\x6c\xc0\x2b\xc0\x2c\xc0\x86\xc0\x87\xc0\x09\xc0\x23\xc0\x0a\xc0\x24\xc0\x72\xc0\x73\xc0\xac\xc0\xad\xc0\x08\xc0\x2f\xc0\x30\xc0\x8a\xc0\x8b\xc0\x13\xc0\x27\xc0\x14\xc0\x28\xc0\x76\xc0\x77\xc0\x12\x00\x9c\x00\x9d\xc0\x7a\xc0\x7b\x00\x2f\x00\x3c\x00\x35\x00\x3d\x00\x41\x00\xba\x00\x84\x00\xc0\xc0\x9c\xc0\x9d\x00\x0a\x00\x9e\x00\x9f\xc0\x7c\xc0\x7d\x00\x33\x00\x67\x00\x39\x00\x6b\x00\x45\x00\xbe\x00\x88\x00\xc4\xc0\x9e\xc0\x9f\x00\x16\x01\x00\x00\x70\x00\x17\x00\x00\x00\x16\x00\x00\x00\x05\x00\x05\x01\x00\x00\x00\x00\x00\x00\x00\x13\x00\x11\x00\x00\x0e\x77\x77\x77\x2e\x72\x65\x73\x79\x64\x65\x76\x2e\x66\x72\xff\x01\x00\x01\x00\x00\x23\x00\x00\x00\x0a\x00\x0c\x00\x0a\x00\x17\x00\x18\x00\x19\x00\x15\x00\x13\x00\x0b\x00\x02\x01\x00\x00\x0d\x00\x16\x00\x14\x04\x01\x04\x03\x05\x01\x05\x03\x06\x01\x06\x03\x03\x01\x03\x03\x02\x01\x02\x03\x00\x10\x00\x0b\x00\x09\x08\x68\x74\x74\x70\x2f\x31\x2e\x31'

        parser=TLSHelloParser()
        parser.parseClientHelloHanshake(by)
        self.assertEqual(parser.getTLSVersion(), 0x303)
        self.assertEqual(parser.getHostname(), "www.resydev.fr")
        
    def test_pattern_withtls_1_2_windows(self):
        by = b'\x16\x03\x03\x00\xcf\x01\x00\x00\xcb\x03\x03\x5a\xa2\x40\xe2\xef\x80\xb8\x76\x79\xee\x15\xd3\x40\x83\x9c\x7a\x9a\x10\xae\x7b\x19\x7f\x52\x24\x56\xcf\xe1\x2e\x86\xc5\xd8\xc1\x00\x00\x38\xc0\x2c\xc0\x2b\xc0\x30\xc0\x2f\x00\x9f\x00\x9e\xc0\x24\xc0\x23\xc0\x28\xc0\x27\xc0\x0a\xc0\x09\xc0\x14\xc0\x13\x00\x39\x00\x33\x00\x9d\x00\x9c\x00\x3d\x00\x3c\x00\x35\x00\x2f\x00\x0a\x00\x6a\x00\x40\x00\x38\x00\x32\x00\x13\x01\x00\x00\x6a\x00\x00\x00\x26\x00\x24\x00\x00\x21\x76\x31\x30\x2e\x76\x6f\x72\x74\x65\x78\x2d\x77\x69\x6e\x2e\x64\x61\x74\x61\x2e\x6d\x69\x63\x72\x6f\x73\x6f\x66\x74\x2e\x63\x6f\x6d\x00\x05\x00\x05\x01\x00\x00\x00\x00\x00\x0a\x00\x08\x00\x06\x00\x1d\x00\x17\x00\x18\x00\x0b\x00\x02\x01\x00\x00\x0d\x00\x14\x00\x12\x04\x01\x05\x01\x02\x01\x04\x03\x05\x03\x02\x03\x02\x02\x06\x01\x06\x03\x00\x23\x00\x00\x00\x17\x00\x00\xff\x01\x00\x01\x00'

        parser=TLSHelloParser()
        parser.parseClientHelloHanshake(by)
        self.assertEqual(parser.getTLSVersion(), 0x303)
        self.assertEqual(parser.getHostname(), "v10.vortex-win.data.microsoft.com")


class BlockDomainTest(unittest.TestCase):
    def setUp(self):
        self.blockdomain=BlockDomain("./utests/block_domain.txt",\
                                     "./utests/allow_domain.txt")

    def tearDown(self):
        self.blockdomain.clear()

    def test_blocked_domains(self):
        self.assertFalse(self.blockdomain.isDomainAllowed("test.net"))
        self.assertFalse(self.blockdomain.isDomainAllowed("test1.net"))
        self.assertFalse(self.blockdomain.isDomainAllowed("www.test1.net"))
        self.assertFalse(self.blockdomain.isDomainAllowed("s.s.test1.net"))
        self.assertTrue(self.blockdomain.isDomainAllowed("test.fr"))
        self.assertTrue(self.blockdomain.isDomainAllowed("net.fr"))
        self.assertTrue(self.blockdomain.isDomainAllowed("test1.net.fr"))
        self.assertFalse(self.blockdomain.isDomainAllowed("qwx.fr"))
        self.assertFalse(self.blockdomain.isDomainAllowed("qwx.fr"))
        self.assertFalse(self.blockdomain.isDomainAllowed("qwx.com"))
        self.assertTrue(self.blockdomain.isDomainAllowed("abcdef.qwx.fr"))
        self.assertTrue(self.blockdomain.isDomainAllowed("abcdef.gtf.com"))

    def test_isDomainAllowed(self):
        self.blockdomain.decisionDicCache.clear()
        self.blockdomain.domainTableCache.clear()
        self.blockdomain.blocklist.clear()
        self.blockdomain.blocklist.append("net.fr")
        self.assertTrue(self.blockdomain.isDomainAllowed("test.internet.fr"))
        self.blockdomain.blocklist.append("internet.fr")
        self.blockdomain.decisionDicCache.clear()
        self.blockdomain.domainTableCache.clear()
        self.assertFalse(self.blockdomain.isDomainAllowed("test.internet.fr"))

        self.blockdomain.blocklist.append("forbid.internet2.fr")
        self.assertTrue(self.blockdomain.isDomainAllowed("internet2.fr"))
        self.assertTrue(self.blockdomain.isDomainAllowed("allow.internet2.fr"))
        self.assertFalse(self.blockdomain.isDomainAllowed("forbid.internet2.fr"))
        self.assertFalse(self.blockdomain.isDomainAllowed("no.forbid.internet2.fr"))
        self.blockdomain.decisionDicCache.clear()
        self.blockdomain.domainTableCache.clear()
        self.blockdomain.allowlist.append("internet2.fr")
        self.assertTrue(self.blockdomain.isDomainAllowed("no.forbid.internet2.fr"))
        self.assertTrue(self.blockdomain.isDomainAllowed("internet2.fr"))
        self.blockdomain.blocklist.append(".net")
        self.assertFalse(self.blockdomain.isDomainAllowed("test.net"))

    def test_cache(self):
        # filled the cache
        self.blockdomain.isDomainAllowed("test.net")
        self.blockdomain.isDomainAllowed("test1.net")
        self.blockdomain.isDomainAllowed("www.test1.net")
        self.blockdomain.isDomainAllowed("s.s.test1.net")
        self.blockdomain.isDomainAllowed("test.fr")
        self.blockdomain.isDomainAllowed("net.fr")
        self.blockdomain.isDomainAllowed("test1.net.fr")
        # test cache
        self.assertEqual(len(self.blockdomain.decisionDicCache), 7)
        self.assertEqual(len(self.blockdomain.domainTableCache), 7)
        self.assertFalse(self.blockdomain.isDomainAllowed("test.net")) # in cache
        self.assertEqual(len(self.blockdomain.decisionDicCache), 7)
        self.assertEqual(len(self.blockdomain.domainTableCache), 7)
        # test purge
        self.blockdomain.limitsizeoftable=7
        self.assertFalse(self.blockdomain.isDomainAllowed("test3.net"))
        self.assertFalse(self.blockdomain.isDomainAllowed("test4.net"))
        self.assertEqual(len(self.blockdomain.decisionDicCache), 7)
        self.assertEqual(len(self.blockdomain.domainTableCache), 7)
        self.assertTrue("test4.net" in self.blockdomain.domainTableCache)
        self.assertTrue("test.fr" in self.blockdomain.domainTableCache)
        self.assertTrue("www.test1.net" in self.blockdomain.domainTableCache)
        self.assertFalse("test1.net" in self.blockdomain.domainTableCache)
        self.assertFalse("test.net" in self.blockdomain.domainTableCache)
        self.assertTrue("test4.net" in self.blockdomain.decisionDicCache)
        self.assertTrue("test.fr" in self.blockdomain.decisionDicCache)
        self.assertTrue("www.test1.net" in self.blockdomain.decisionDicCache)
        self.assertFalse("test1.net" in self.blockdomain.decisionDicCache)
        self.assertFalse("test.net" in self.blockdomain.decisionDicCache)

    def test_filter_policy(self):
        self.blockdomain.clear()
        self.blockdomain.filter_policy=0 # allowlist, blocklist, accept
        self.blockdomain.blocklist.append(".net")
        self.blockdomain.allowlist.append("internet.net")
        self.assertTrue(self.blockdomain.isDomainAllowed("internet.fr")) # not in lists, default policy = accept
        self.assertTrue(self.blockdomain.isDomainAllowed("www.internet.net")) # allowlist > blocklist
        self.assertFalse(self.blockdomain.isDomainAllowed("www.resydev.net")) # not in allowlist ; in blocklist

        self.blockdomain.clear()
        self.blockdomain.filter_policy=1 # blocklist, allowlist, accept
        self.blockdomain.allowlist.append(".net")
        self.blockdomain.blocklist.append("internet.net")
        self.assertTrue(self.blockdomain.isDomainAllowed("internet.fr")) # not in lists, default policy = accept
        self.assertFalse(self.blockdomain.isDomainAllowed("www.internet.net")) # blocklist > allowlist
        self.assertTrue(self.blockdomain.isDomainAllowed("www.resydev.net")) # not in blocklist ; in allowlist

        self.blockdomain.clear()
        self.blockdomain.filter_policy=2 # allowlist, blocklist, reject
        self.blockdomain.blocklist.append(".net")
        self.blockdomain.allowlist.append("internet.net")
        self.assertFalse(self.blockdomain.isDomainAllowed("internet.fr")) # not in lists, default policy = reject
        self.assertTrue(self.blockdomain.isDomainAllowed("www.internet.net")) # allowlist > blocklist
        self.assertFalse(self.blockdomain.isDomainAllowed("www.resydev.net")) # not in allowlist ; in blocklist

        self.blockdomain.clear()
        self.blockdomain.filter_policy=3 # blocklist, allowlist, reject
        self.blockdomain.allowlist.append(".net")
        self.blockdomain.blocklist.append("internet.net")
        self.assertFalse(self.blockdomain.isDomainAllowed("internet.fr")) # not in lists, default policy = reject
        self.assertFalse(self.blockdomain.isDomainAllowed("www.internet.net")) # blocklist > allowlist
        self.assertTrue(self.blockdomain.isDomainAllowed("www.resydev.net")) # not in blocklist ; in allowlist

class LogsTest(unittest.TestCase):
    def setUp(self):
        self.filename="./utests/test.log"
        self.log=Logs(False, self.filename, 10000, 4, True, True)
    
    def tearDown(self):
        try:
           os.remove(self.filename)
        except:
           pass

    def getLinesFromFiles(self):
        buff=""
        with open(self.filename, 'r') as fd:
            buff+=fd.read()
        return buff
        
    def test_logConnect(self):
        self.log.logConnect('192.168.1.1', 'www.test.fr')
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 2)
        self.assertTrue('192.168.1.1' in lines)
        self.assertTrue('www.test.fr' in lines)
        self.assertTrue('CONNECT' in lines)
        self.assertTrue('[INFO]' in lines)

    def test_logConnectDisable(self):
        self.log.logconnect=False
        self.log.logConnect('192.168.1.2', 'www.test2.fr')
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 1)
        self.assertFalse('192.168.1.2' in lines)
        self.assertFalse('www.test2.fr' in lines)
        self.assertFalse('CONNECT' in lines)
        self.assertFalse('[INFO]' in lines)

    def test_logBlocked(self):
        self.log.logBlocked('192.168.1.3', 'www.test3.fr')
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 2)
        self.assertTrue('192.168.1.3' in lines)
        self.assertTrue('www.test3.fr' in lines)
        self.assertTrue('BLOCKED' in lines)
        self.assertTrue('[WARNING]' in lines)

    def test_logBlockedDisable(self):
        self.log.logblocked=False
        self.log.logBlocked('192.168.1.4', 'www.test4.fr')
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 1)
        self.assertFalse('192.168.1.4' in lines)
        self.assertFalse('www.test4.fr' in lines)
        self.assertFalse('BLOCKED' in lines)
        self.assertFalse('[WARNING]' in lines)

    def test_logServices(self):
        payload='ABCDEFGHIJK'
        self.log.logServices(payload)
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 2)
        self.assertTrue(payload in lines)

    def test_logCache(self):
        self.log.wait=0.8
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        lines=self.getLinesFromFiles()
        self.assertEqual(len(lines.split('\n')), 2)
        self.assertTrue('192.168.1.1' in lines)
        self.assertTrue('www.test.fr' in lines)
        self.assertTrue('BLOCKED' in lines)
        self.assertTrue('[WARNING]' in lines)
        time.sleep(1.2)
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        lines=self.getLinesFromFiles()
        lines=lines.split('\n')
        self.assertEqual(len(lines), 3)
        self.assertTrue('192.168.1.1' in lines[1])
        self.assertTrue('www.test.fr' in lines[1])
        self.assertTrue('BLOCKED' in lines[1])
        self.assertTrue('[WARNING]' in lines[1])
        self.assertEqual(len(self.log.cacheDic), 1)
        self.assertEqual(len(self.log.cacheTable), 1)

    def test_logPurgeCache(self):
        self.log.wait=0
        self.log.limitsizeoftable=2
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        self.log.logBlocked('192.168.1.1', 'www.test.fr')
        self.log.logBlocked('192.168.1.2', 'www.test.fr')
        self.log.logBlocked('192.168.1.2', 'www.test2.fr')
        self.assertEqual(len(self.log.cacheDic), 2)
        self.assertEqual(len(self.log.cacheTable), 2)
        self.assertTrue(('192.168.1.2', 'www.test2.fr') in self.log.cacheDic)
        self.assertTrue(('192.168.1.2', 'www.test.fr') in self.log.cacheDic)
        self.assertFalse(('192.168.1.1', 'www.test.fr') in self.log.cacheDic)
        self.assertTrue(('192.168.1.2', 'www.test2.fr') in self.log.cacheTable)
        self.assertTrue(('192.168.1.2', 'www.test.fr') in self.log.cacheTable)
        self.assertFalse(('192.168.1.1', 'www.test.fr') in self.log.cacheTable)

if __name__ == '__main__':
    unittest.main()




