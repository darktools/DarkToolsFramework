import argparse

from nameko.rpc import rpc

from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def nmap_tcp_ports(sProject, sUniqSelectorId, sDomain, sIpAddy, sPorts, sSourceTool):
    lOpenTcpPorts = []
    try:
        sCmdToExecute = '/usr/bin/nmap -Pn -n -sT -p '+sPorts+' --reason ' + sIpAddy
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.info(""+sSourceTool+"() sCmdOut: " + str(sCmdOut))
        sSeverity = "INFO"
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sSourceTool+"() subprocess.Popen failed :\ ")
    try:
        logging.info("sCmdOut: " + str(sCmdOut))
        lCmdOut = sCmdOut.splitlines()
        logging.info("lCmdOut: " + str(lCmdOut))
        for sLine in lCmdOut:
            sLine = sLine.strip()
            logging.info("sLine: " + str(sLine))
            #
            sPortStringToFind = '/tcp'
            #
            if sLine.find(sPortStringToFind) >= 0:
                sPort = sLine[:sLine.find(sPortStringToFind)]
                lSections = sLine.split()
                sState = lSections[1]
                sService = lSections[2]
                sReason = lSections[3]
                if sState.find("open") >= 0:
                    logging.info("sPort: " + str(sPort))
                    lOpenTcpPorts.append(sPort)
                    logging.info("lOpenTcpPorts: " + str(lOpenTcpPorts))
                    jEvent = {
                        "project": sProject,
                        "dest": sIpAddy,
                        "port": sPort,
                        "state": sState,
                        "uniq_selector_id": sUniqSelectorId,
                        "domain": sDomain,
                        "severity": sSeverity
                    }
                    splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
        logging.error("[ERROR] str(Exception): " + str(e))
    lOpenTcpPorts = sortUniqList(lOpenTcpPorts)
    return lOpenTcpPorts

def interesting_tcpports(sProject, sUniqSelectorId, sDomain, sIpAddy):
    lOpenTcpPorts = []
    try:
        lTcpPortsToCheck = ['0',     # If they are crazy enough to use this port we should check it out
                  '21',    # FTP
                  '22',    # SSH
                  '23',    # Telnet
                  '25',    # SMTP
                  '53',    # DNS
                  '69',    # TFTP
                  '80',    # Web
                  '111',   # RPC
                  '123',   # NTP
                  '135',   # NetBIOS / SMB
                  '139',   # NetBIOS / SMB
                  '143',   # IMAP
                  '389',   # LDAP
                  '443',   # Web
                  '445',   # NetBIOS / SMB
                  '636',   # LDAP
                  '1433',  # MSSQL DB
                  '2082',  # Web / cPanel
                  '2083',  # Web / cPanel SSL
                  '2086',  # Web / WHM / cPanel
                  '2087',  # Web / WHM SSL / cPanel SSL
                  '2181',  # ZooKeeper
                  '3306',  # MySQL DB
                  '3389',  # RDP
                  '4502',  # Web / AEM
                  '4503',  # Web / AEM
                  '5050',  # Mesos Master
                  '5051',  # Mesos Agent
                  '5432',  # Postgres
                  '5666',  # NRPE
                  '5900',  # VNC
                  '5901',  # VNC
                  '5902',  # VNC
                  '5984',  # CouchDB
                  '6379',  # Redis
                  '7199',  # JMX
                  '8000', # Web / Splunk Search Web UI
                  '8080',  # Web
                  '8081',  # Web
                  '8089', # Splunk Universal Forwarder / splunkd / Deployment Server
                  '8181',  # Web / DC\OS Zookeeper
                  '8443',  # Web
                  '8649',  # Ganglia / gmetad
                  '8651',  # Ganglia / gmond
                  '8660',  # Ganglia / gmond
                  '8661',  # Ganglia / gmond
                  '8662',  # Ganglia / gmond
                  '8888',  # Web
                  '9997',  # Splunk forwarders to the Splunk indexer
                  '10000', # Web / Webmin
                  '11211', # Memcached
                  '27017', # MongoDB
                  '27018', # MongoDB
                  '27019', # MongoDB
                  '50070', # Hadoop
                  #'50075',  # Hadoop
                  #'50090',  # Hadoop
                  #'50105',  # Hadoop
                  #'50030',  # Hadoop
                  #'50060',  # Hadoop
                  '65535'] # If they are crazy enough to use this port we should check it out
        sTcpPortsToCheck = ",".join(lTcpPortsToCheck)
        sSourceTool = 'nmapinteresting_tcpports'
        lNewOpenTcpPorts = nmap_tcp_ports(sProject, sUniqSelectorId, sDomain, sIpAddy, sTcpPortsToCheck, sSourceTool)
        lOpenTcpPorts = lOpenTcpPorts + lNewOpenTcpPorts
    except Exception as e:
        logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
        logging.error("[ERROR] str(Exception): " + str(e))
        logging.error(""+sSourceTool+"() subprocess.Popen failed :\ ")
    return lOpenTcpPorts

def all_tcpports(sProject, sUniqSelectorId, sDomain, sIpAddy):
    sSourceTool = 'masscanall_tcpports'
    lOpenTcpPorts = []
    try:
        sCmdToExecute = '/usr/bin/masscan -p0-65535 ' + sIpAddy + '/32'
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug("" + sSourceTool + "() sCmdOut: " + str(sCmdOut))
        sSeverity = "INFO"
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sSourceTool + "() subprocess.Popen failed :\ ")

    try:
        logging.debug("sCmdOut: " + str(sCmdOut))
        lCmdOut = sCmdOut.splitlines()
        logging.debug("lCmdOut: " + str(lCmdOut))
        for sLine in lCmdOut:
            sLine = sLine.strip()
            logging.debug("sLine: " + str(sLine))
            sStringToFind = 'Discovered open port '
            sPortStringToFind = '/tcp'
            if sLine.find(sPortStringToFind) >= 0:
                lSections = sLine.split()
                sPort = lSections[3]
                lPort =  sPort.split("/")
                sPort = lPort[0]
                logging.debug("sPort: " + str(sPort))
                #
                lOpenTcpPorts.append(sPort)
                logging.info("lOpenTcpPorts: " + str(lOpenTcpPorts))
                jEvent = {
                    "project": sProject,
                    "dest": sIpAddy,
                    "port": sPort,
                    "state": "open",
                    "uniq_selector_id": sUniqSelectorId,
                    "domain": sDomain,
                    "severity": sSeverity
                }
                splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
        logging.error("[ERROR] str(Exception): " + str(e))
    lOpenTcpPorts = sortUniqList(lOpenTcpPorts)
    return lOpenTcpPorts

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def find_open_tcp_ports(sProject, sUniqSelectorId, sDomain, sIp):
    getToLogging()
    #
    sIpAddy = sIp.strip()
    lInterestingOpenTcpPorts = interesting_tcpports(sProject, sUniqSelectorId, sDomain, sIpAddy)
    lAllOpenTcpPorts = all_tcpports(sProject, sUniqSelectorId, sDomain, sIpAddy)
    #
    lOpenTcpPorts = lInterestingOpenTcpPorts + lAllOpenTcpPorts
    lOpenTcpPorts = sortUniqList(lOpenTcpPorts)
    #
    return lOpenTcpPorts

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class ServiceReconFindOpenTcpPorts:
    name = "service_recon_find_open_tcp_ports"

    @rpc
    def remote_method(self, sProject, sUniqSelectorId, sDomain, sIp):
        return find_open_tcp_ports(sProject, sUniqSelectorId, sDomain, sIp)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
standalone 
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a")  # project name
    parser.add_argument("-b")  # ip
    parser.add_argument("-c")  # port
    parser.add_argument("-d")  # ip
    args, leftovers = parser.parse_known_args()
    if args.a is not None:
        print "a has been set (value is %s)" % args.a
        print "b has been set (value is %s)" % args.b
        print "c has been set (value is %s)" % args.c
        print "d has been set (value is %s)" % args.d
        lOpenTcpPorts = find_open_tcp_ports(args.a, args.b, args.c, args.d)
        print("lOpenTcpPorts: " + str(lOpenTcpPorts))

main()