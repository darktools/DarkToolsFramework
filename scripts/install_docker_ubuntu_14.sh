#!/bin/bash
#
# Install Docker on Ubuntu 14.04 x64
#
# Usage:
# sudo su -
# curl https://gist.githubusercontent.com/TweekFawkes/.../raw.../install_docker_ubuntu_14_04 | bash
#
# Author: @TweekFawkes
#
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-get -y install curl
apt-get -y install linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get -y install docker-ce
docker run hello-world