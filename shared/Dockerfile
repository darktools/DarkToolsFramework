FROM ubuntu:16.04

MAINTAINER TweekFawkes

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get -y install python-pip

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install iputils-ping
RUN apt-get update && apt-get -y install nmap
RUN apt-get update && apt-get -y install whois
RUN apt-get update && apt-get -y install traceroute
RUN apt-get update && apt-get -y install curl
RUN apt-get update && apt-get -y install wget
RUN apt-get update && apt-get -y install git
RUN apt-get update && apt-get -y install perl

RUN pip install pyzmq-static

RUN pip install netaddr

RUN apt-key adv --keyserver pgp.mit.edu --recv-keys ED444FF07D8D0BF6
RUN echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
RUN apt-get update -m

# dnsrecon
#RUN apt-get update && apt-get -y install dnsrecon
#RUN mkdir -p /opt/wordlists/
#RUN cd /opt/wordlists/ && wget --no-check-certificate https://github.com/kkirsche/wordlistgenerator/raw/master/dnsmap.txt

# udp-proto-scanner
RUN cd /opt/ && git clone https://github.com/portcullislabs/udp-proto-scanner.git

# amap
RUN apt-get update && apt-get -y install amap

# gobuster
RUN apt-get update && apt-get -y install gobuster
#RUN cd /opt/ && git clone https://github.com/OJ/gobuster.git
RUN mkdir -p /opt/wordlists/
RUN cd /opt/wordlists/ && wget --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web_Content/quickhits.txt
RUN cat /opt/wordlists/quickhits.txt | cut -c 2- >> /opt/wordlists/quickhits_noslash.txt
RUN cd /opt/wordlists/ && wget --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/sorted_knock_dnsrecon_fierce_recon-ng.txt
RUN cat /opt/wordlists/sorted_knock_dnsrecon_fierce_recon-ng.txt | tr A-Z a-z | sort -u > /opt/wordlists/sort_uniq_knock_dnsrecon_fierce_recon-ng.txt

# dnscan
RUN apt-get -y update && apt-get -y install python-dnspython
RUN cd /opt && git clone https://github.com/rbsec/dnscan.git && cd /opt/dnscan/

# ip to city
#RUN cd /opt && git clone https://github.com/artemdinaburg/ip-to-city.git
#RUN cd /opt/ip-to-city && wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz -O /opt/ip-to-city/GeoLiteCity.dat.gz && gunzip --force /opt/ip-to-city/GeoLiteCity.dat.gz

# domian name whois via pythonwhois
RUN pip install pythonwhois

# ipwhois
RUN pip install ipwhois

# theHarvestor
RUN cd /opt && git clone https://github.com/laramies/theHarvester.git

# masscan
RUN apt-get -y update && apt-get -y install masscan

# testssl.sh
RUN apt-get update && apt-get -y install dnsutils
RUN apt-get update && apt-get -y install ldnsutils
RUN apt-get update && apt-get -y install bsdmainutils
RUN apt-get update && apt-get -y install ca-certificates
RUN cd /opt && git clone https://github.com/drwetter/testssl.sh.git

# hydra
RUN apt-get update && apt-get -y install hydra
RUN wget -O /opt/wordlists/top_shortlist_of_usernames.txt --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/8ef86942566bb1ff332330bb2b9f30b0952605ed/Usernames/top_shortlist.txt
#RUN wget -O /opt/wordlists/top_shortlist_of_passwords.txt --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/8ef86942566bb1ff332330bb2b9f30b0952605ed/Passwords/top_shortlist.txt
RUN wget -O /opt/wordlists/top_shortlist_of_passwords.txt --no-check-certificate https://gist.githubusercontent.com/TweekFawkes/37267f9ea4e36ca73e2a40791b4e2be5/raw/6af78f9d88354f3fb041332db0b579232c7c4435/ssh_passwords
RUN wget -O /opt/wordlists/conficker.txt --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/conficker.txt
RUN wget -O /opt/wordlists/top-20-common-SSH-passwords.txt --no-check-certificate https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/top-20-common-SSH-passwords

COPY . /app

RUN chmod +x /app/*.sh

#CMD /app/debug.sh

