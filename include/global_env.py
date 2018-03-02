#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Daniel Rocher <daniel.rocher@resydev.fr>
# Copyright (C) 2018

import sys

class Global(object):
    pass

    @staticmethod
    def debug(msg):
        """print a debug message"""
        if Global.debug_fwdproxy:
            print (msg)

    @staticmethod
    def error(msg):
        """print an error message"""
        sys.stderr.write("\n{}\n".format(msg))

#variables environments
Global.progname="fwdproxyd"
Global.version_fwdproxyd="0.7.3"
Global.date_fwdproxyd="2018-03-01"

# default value
Global.config_filename='/etc/fwdproxyd/fwdproxyd.conf'
Global.debug_fwdproxy=False # view debug messages
Global.default_port_server=8080 # TCP port
Global.current_port_server=Global.default_port_server
Global.daemonize=False
Global.filename_bkl=None # filename of blacklisted domain


if __name__ == "__main__":
    print ("Version of {}: {}\nDate: {}".format(Global.progname, Global.version_fwdproxyd, Global.date_fwdproxyd))

