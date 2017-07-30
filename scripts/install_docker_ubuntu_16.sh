#!/bin/bash
#
# Install Docker on Ubuntu 16.04 x64
#
# Usage:
# sudo su -
# curl https://gist.githubusercontent.com/TweekFawkes/.../raw.../install_docker_ubuntu_16_04 | bash
#
# Author: @TweekFawkes
#
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
apt-get update
apt-get install -y docker-engine
docker run hello-world