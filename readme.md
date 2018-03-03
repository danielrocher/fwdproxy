
# FwdProxy - A Transparent Filtering Proxy

**Experimental**

_This program is licensed to you under the terms of the GNU General Public License version 3_

## Features

 - HTTP/HTTPS transparent proxy
 - ability to filter domain names (http/https)
 - no external modules required
 - support http redirection (HTTP/1.1 302)

## Future

 - add ipv6 support
 - logging


## Installation

FwdProxy requires : python >= 3.2, Openssl

On Debian/Ubuntu :

    sudo apt-get install python3 openssl
    git clone https://github.com/danielrocher/fwdproxy.git
    cd fwdproxy
    sudo make install


Edit */etc/fwdproxyd/fwdproxyd.conf* at your convenience. Example :

    [Global]
    
    # port number
    # default port=8080
    port=8080
    
    [Filtering]
    # domain blacklist file
    blacklist_domain_filename=
    
    # enable redirection if domain is blocked (HTTP 1/1 302)
    enable_redirect=true
    
    # template file for redirection
    keywords availables in file template: $redirect$ (url_redirect), $date$, $length$, $domain$
    # template_file_redirect=templates/redirect.txt
    
    # url for redirection
    # keyword available : $domain$
    url_redirect=http://www.yourdomainnameexist.com/?blacklisted=$domain$



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

    curl -I -v --header "Host: test.fr"  http://127.0.0.1:8080

### test proxy with https

    openssl s_client -connect 127.0.0.1:8080 -servername www.test.fr
    openssl s_client -connect 127.0.0.1:8080 -servername www.test.fr -tls1
    openssl s_client -connect 127.0.0.1:8080 -servername www.test.fr -tls1_1


