
# FwdProxy - A Transparent Filtering Proxy

**Experimental**

_This program is licensed to you under the terms of the GNU General Public License version 3_

## Installation

FwdProxy requires : python >= 3.2, Openssl

On Debian/Ubuntu :

    sudo apt-get install python3 openssl
    cd fwdproxyd
    sudo make install


Edit */etc/fwdproxyd/fwdproxyd.conf* at your convenience. Example :

    [GLOBAL]

    # port number
    # default port=8080
    port=8080

    [FILTERING]

    # filename of blacklisted domain
    blacklist_domain_filename=

## Start service :

    sudo systemctl start fwdproxyd.service

## Configure iptables

Forward **http** and **https** traffic to proxy (example):

    iptables -t nat -A PREROUTING -s 192.168.58.0/24 -p tcp --dport 80  -j REDIRECT --to 8080
    iptables -t nat -A PREROUTING -s 192.168.58.0/24 -p tcp --dport 443 -j REDIRECT --to 8080

## Usage

    ./fwdproxyd -h
    
    	Usage:  fwdproxyd -c <filename> -d -m -p <port> -v --help
    
    	-h| --help :    Show this help
    	-d :            Daemonize
    	-c <filename> : Configuration filename
    	-b <filename> : Domain blacklist file
    	-p <port> :     TCP port - default = 8080
    	-v| --version : Show fwdproxyd version
    	-m :            Show debug messages

## Uninstall

    sudo make uninstall

## Tests

### test proxy with http

    curl -I -v --header "Host: resydev.fr"  http://127.0.0.1:8080

### test proxy with https

    openssl s_client -connect 127.0.0.1:8080 -servername www.resydev.fr
    openssl s_client -connect 127.0.0.1:8080 -servername www.resydev.fr -tls1
    openssl s_client -connect 127.0.0.1:8080 -servername www.resydev.fr -tls1_1


