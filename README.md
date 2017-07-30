8 888888888o.            .8.          8 888888888o.   8 8888     ,88' 8888888 8888888888 ,o888888o.         ,o888888o.     8 8888           d888888o.
8 8888    `^888.        .888.         8 8888    `88.  8 8888    ,88'        8 8888    . 8888     `88.    . 8888     `88.   8 8888         .`8888:' `88.
8 8888        `88.     :88888.        8 8888     `88  8 8888   ,88'         8 8888   ,8 8888       `8b  ,8 8888       `8b  8 8888         8.`8888.   Y8
8 8888         `88    . `88888.       8 8888     ,88  8 8888  ,88'          8 8888   88 8888        `8b 88 8888        `8b 8 8888         `8.`8888.
8 8888          88   .8. `88888.      8 8888.   ,88'  8 8888 ,88'           8 8888   88 8888         88 88 8888         88 8 8888          `8.`8888.
8 8888          88  .8`8. `88888.     8 888888888P'   8 8888 88'            8 8888   88 8888         88 88 8888         88 8 8888           `8.`8888.
8 8888         ,88 .8' `8. `88888.    8 8888`8b       8 888888<             8 8888   88 8888        ,8P 88 8888        ,8P 8 8888            `8.`8888.
8 8888        ,88'.8'   `8. `88888.   8 8888 `8b.     8 8888 `Y8.           8 8888   `8 8888       ,8P  `8 8888       ,8P  8 8888        8b   `8.`8888.
8 8888    ,o88P' .888888888. `88888.  8 8888   `8b.   8 8888   `Y8.         8 8888    ` 8888     ,88'    ` 8888     ,88'   8 8888        `8b.  ;8.`8888
8 888888888P'   .8'       `8. `88888. 8 8888     `88. 8 8888     `Y8.       8 8888       `8888888P'         `8888888P'     8 888888888888 `Y8888P ,88P'

Alpha v0.0.1 Release!

A PENTESTERS GUIDE TO PWNAGE VISUALIZATION

I. Background

This is the alpha release of the DarkTools framework.

Designed from the ground up to visualize within Splunk output from common penetration testing tools.

It currently features:
- automating common penetration testing tasks
- normalizing the output into JSON objects
- sending the data to Splunk's HTTP Event Collector (HEC)
- leveraging a highly distributed microservices based architecture on the backend
- chaining of reconnaissance tasks to enable full automation of testing all targets under a single root domain
- visualization of the data being sent into Splunk via the DarkTools Splunk App

The alpha release still has some drawbacks that I hope to address in the next version.

Please see our BlackHat presentation for more information behind this tool.


II. Usage

II. A. Quick Setup and Development

Example of Setting Up the Framework for Local or Development Usage

I tested this using a Kali Linux 2017.1 VM running within VMware Fusion

$ md5 Kali-Linux-2017.1-vm-amd64.7z
MD5 (Kali-Linux-2017.1-vm-amd64.7z) = 56b79dddb6f9c8ae71d2119c395ecd21

- Setup Splunk w/ HEC with an Index for "DarkTools"
- Install the Splunk "DarkTools" App
- Run the all in one script... ./run_all_with_console.sh


II. B. Production

Example of Building the Framework for Production Highly Distributed Usage


II. B. i. Supporting Systems

We need to get a few supporting systems in place for this to all work


II. B. i. a. Splunk

- You will need a Splunk Server with the HTTP Event Collector (HEC) Enabled.
- Create an index within Splunk called "darktools".
- Generate a HEC Key to be used with the DarkTools Framework.
- Ensure the microservices can send data to the HEC (e.g. AWS Security Groups ACL configuration)


II. B. i. a. Private Docker Registry

- Setup a Server

I deployed within AWS Ubuntu 16.04 x64 server onto a t2.small instance
AMI ID: ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20170619.1 (ami-73f7da13)


- Configure ACLs

I reconfigured the security groups to all 22 from my IP with HTTP & HTTPS open to the servers with the microservices


- FQDNs

I pointed a subdomain to my EC2 instance (e.g. hub.darkgrifter.com)


- Install Docker w/ Let's Encrypt

chmod +x scripts/install_docker_ubuntu_16.sh
./scripts/install_docker_ubuntu_16.sh

docker pull registry:2
mkdir /opt/registryData
# Insecure # docker run -d -p 5000:5000 -v /opt/data:/var/lib/registry registry:2
cd /opt/
apt-get -y install git
git clone https://github.com/letsencrypt/letsencrypt.git
cd letsencrypt
./letsencrypt-auto certonly --keep-until-expiring --standalone -d hub.darkgrifter.com --email info@hub.darkgrifter.com

line="30 2 * * 1 /opt/letsencrypt/letsencrypt-auto renew >> /var/log/letsencrypt-renew.log"
(crontab -u root -l; echo "$line" ) | crontab -u root -

cd /etc/letsencrypt/live/hub.darkgrifter.com/
cp privkey.pem domain.key
cat cert.pem chain.pem > domain.crt
chmod 777 domain.crt
chmod 777 domain.key

docker run -d -p 443:5000 --restart=always --name registry \
  -v /etc/letsencrypt/live/hub.darkgrifter.com:/certs \
  -v /opt/registryData:/var/lib/registry \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2

See references section below for more information on how to set this up


II. B. ii. Build

- change into the Usage containing the code:
git clone ...
cd DarkToolsFramework

- edit configuration file:
vi shared/config.yaml
HEC_URL: 'https://ip.of.splunk.hec:8088/services/collector'
HEC_KEY: 'TOKEN-TOKEN-TOKEN-TOKEN-TOKEN'
AMQP_PROTO: 'amqp://'
AMQP_SERVER: 'ip.of.mq.microservice'
AMQP_PORT: '5672'

- optionally delete all docker containers on the build system:
./scripts/clean_docker_everything.sh

- build using the build script:
python pushDarkTools.py -e stage -r hub.darkgrifter.com


II. B. iii. Run the DarkTools Framework

Example of Running the Framework for Production Highly Distributed Usage

- I then create an SSH tunnel to my splunk server via a command like:
ssh -N -D 9050 -i ~/ssh_private_key.pem ubuntu@ip.of.splunk.server

- I then setup FoxyProxy within FireFox to use the SSH tunnel via an SOCKSv4 proxy on TCP port 9050
URL: https://127.0.0.1:8000/
Username: admin
Password: redacted_strong_pasword


III. References

- This blog inspired the overall design of the project...
http://brunorocha.org/python/microservices-with-python-rabbitmq-and-nameko.html

- Many StackOverflow articles helped out when I need a quick snippet of code, including but not limited to...
https://stackoverflow.com/questions/1885525/how-do-i-prompt-a-user-for-confirmation-in-bash-script

- Private Docker Registry
https://docs.docker.com/registry/deploying/
https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04
https://gist.github.com/PieterScheffers/63e4c2fd5553af8a35101b5e868a811e
https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04
https://www.trainingdevops.com/insights-and-tutorials/deploying-docker-registry-with-let-s-encrypt-ssl-tls-certs
