from nameko.standalone.rpc import ClusterRpcProxy

import argparse
import logging
import os
import time
import traceback

import hashlib  # getUniqId()
import sys  # getUniqId()
import random  # getUniqId()
import string  # getUniqId()
import hashlib  # getHashOfString()

import yaml
import cmd

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

banner_Str = """
                                                                                                                                                    
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

"""


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename="logs/" + str(int(time.time())) + '-' + sScriptName + '.log',
                    filemode='w')
logger = logging.getLogger(__name__)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def sortUniqList(lMyList):
    lMyList = sorted(set(lMyList))
    return lMyList

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


def getTimeMillSec():
    millis = int(round(time.time() * 1000))
    return str(millis)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def randomword(iLength):
    return ''.join(random.choice(string.lowercase) for i in range(iLength))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def getUniqId():
    return str(hashlib.sha384((getTimeMillSec() + randomword(int('33')))).hexdigest())

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def getListFromFile(sFileNameFFP):
    with open(sFileNameFFP) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def cleanUpFile(sFileName):
    os.system("sed '/^$/d' " + sFileName + " > " + sFileName + ".tmp")
    os.system("mv " + sFileName + ".tmp " + sFileName)
    os.system("cat " + sFileName + " | sort -u > " + sFileName + ".tmp")
    os.system("mv " + sFileName + ".tmp " + sFileName)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son(sProject):
    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    config = {
        'AMQP_URI': cfg['AMQP_URI']
    }

    sTargetsFile = "targets.txt"

    fKill = 0
    iSleepTime = 60 * 60 * 24  # seconds * minutes * hours = 4 hours

    while (fKill < 1):
        with open(sTargetsFile) as fhTargetsFile:
            for sLine in fhTargetsFile:
                sLine = sLine.strip()
                lLine = sLine.split(",")
                sProjectInLineOfFile = lLine[0]
                sPrimarySelector = lLine[1]
                sPrimarySelector = sPrimarySelector.strip()
                sSelectorType = lLine[2]
                sSelectorType = sSelectorType.strip()
                logging.debug("000 sSelectorType: " + str(sSelectorType))
                if "rootDomain" in sSelectorType:
                    sRootDomain = sPrimarySelector
                    sUniqSelectorId = getUniqId()
                    logging.debug("000 sRootDomain: " + str(sRootDomain))
                    logging.debug("000 sProjectInLineOfFile: " + str(sProjectInLineOfFile))
                    if sProject == sProjectInLineOfFile:
                        logging.debug("000 sProject: " + str(sProject))
                        with ClusterRpcProxy(config) as cluster_rpc:
                            sScriptName = os.path.basename(__file__)
                            logging.info("001 START: autoPilot.py")
                            lAllDomains = cluster_rpc.service_recon_find_subs.remote_method(sProject, sUniqSelectorId,
                                                                                            sRootDomain)
                            lAllDomains = sortUniqList(lAllDomains)
                            logging.debug("002 lAllDomains: " + str(lAllDomains))
                            random.shuffle(lAllDomains)
                            for sDomain in lAllDomains:
                                logging.debug("003 sDomain: " + str(sDomain))
                                lAllIps = cluster_rpc.service_recon_find_ips.remote_method(sProject, sUniqSelectorId,
                                                                                           sDomain)
                                lAllIps = sortUniqList(lAllIps)
                                logging.debug("004 lAllIps: " + str(lAllIps))
                                random.shuffle(lAllIps)
                                for sIp in lAllIps:
                                    logging.debug("005 sIp: " + str(sIp))
                                    lBlackList = getListFromFile("blacklist_ips.txt")
                                    lWhiteList = getListFromFile("whitelist_ips.txt")
                                    logging.debug("005b lWhiteList: " + str(lWhiteList))
                                    lGrayList = getListFromFile("graylist_ips.txt")
                                    if cluster_rpc.service_validate_ip.remote_method(sProject, sIp, lBlackList, lWhiteList, lGrayList) is True:
                                        logging.debug("006 validate_ip(sIp) is cool, sIp: " + str(sIp))
                                        lAllOpenTcpPorts = cluster_rpc.service_recon_find_open_tcp_ports.remote_method(
                                            sProject, sUniqSelectorId, sDomain, sIp)
                                        lAllOpenTcpPorts = sortUniqList(lAllOpenTcpPorts)
                                        logging.debug("007 lAllOpenTcpPorts: " + str(lAllOpenTcpPorts))
                                        random.shuffle(lAllOpenTcpPorts)
                                        for sOpenTcpPort in lAllOpenTcpPorts:
                                            logging.debug("008 sOpenTcpPort: " + str(sOpenTcpPort))
                                            sTcpService = cluster_rpc.service_recon_find_tcp_service.remote_method(sProject,
                                                                                                                   sUniqSelectorId,
                                                                                                                   sDomain,
                                                                                                                   sIp,
                                                                                                                   sOpenTcpPort)
                                            logging.debug("009 sTcpService: " + str(sTcpService))
                                            sUniqTargetId = getUniqId()
                                            dTarget = {"project": sProject, "uniq_selector_id": sUniqSelectorId,
                                                       "uniq_target_id": sUniqTargetId, "domain": sDomain, "ip": sIp,
                                                       "protocol": "tcp", "port": sOpenTcpPort, "service": sTcpService}
                                            logging.debug("010 dTarget: " + str(dTarget))
                                            # sReturn = cluster_rpc.service_a.dispatching_method(dTarget)
                                            sReturn = cluster_rpc.smokey.dispatching_method.call_async(dTarget)
                                            logging.debug("011 Sent to dispatcher - sReturn: " + str(sReturn))
                                    else:
                                        logging.debug("012 validate_ip(sIp) is NOT cool, sIp: " + str(sIp))
                elif sSelectorType == "netBlock":
                    logging.debug("013 sPrimarySelector: " + str(sPrimarySelector))
                    # TODO: next release
                elif sSelectorType == "ipAddy":
                    logging.debug("014 sPrimarySelector: " + str(sPrimarySelector))
                    # TODO: next release
            logging.info("END: autoPilot.py")
            with open("autopilot_interval.txt") as fhIntervalFile:
                for sIntervalLine in fhIntervalFile:
                    sIntervalLine = sIntervalLine.strip()
                    iSleepTime = int(sIntervalLine)
                    logging.info("SLEEPING for: " + str(iSleepTime))
                    time.sleep(iSleepTime)
            logging.info("WOKE UP from SLEEPING!")

sBlackListFileName = 'blacklist_ips.txt'
sWhiteListFileName = 'whitelist_ips.txt'
sGrayListFileName = 'graylist_ips.txt'
sConfigFileName = 'config.yaml'

class DarkToolsWorld(cmd.Cmd):
    """Simple command processor example."""

    # --- --- --- #

    def help_showConfig(self):
        print '\n'.join([ 'showConfig',
                           'List the Config File',
                           ])

    def do_showConfig(self, line):
        with open(sConfigFileName, 'r') as f:
            for sLineInFile in f:
                sLineInFile = sLineInFile.strip()
                print(sLineInFile)
        print("---")
        return

    # --- --- --- #

    def help_showBlacklist(self):
        print '\n'.join([ 'showBlacklist',
                           'List the Current Blacklist',
                           ])

    def do_showBlacklist(self, line):
        with open(sBlackListFileName, 'r') as f:
            for sLineInFile in f:
                sLineInFile = sLineInFile.strip()
                print(sLineInFile)
        print("...")
        return

    def help_addToBlacklist(self):
        print '\n'.join([ 'addToBlackList [129.123.0.0/16 # Utah State University]',
                           'Add an entry to the Blacklist',
                           ''])

    def do_addToBlacklist(self, line):
        print("line: " + str(line))
        with open(sBlackListFileName, "a") as myfile:
            myfile.write("\n")
            myfile.write(line)
        cleanUpFile(sBlackListFileName)
        print("---")
        return

    # --- --- --- #

    def help_showWhitelist(self):
        print '\n'.join([ 'showWhitelist',
                           'List the Current Whitelist',
                           ])

    def do_showWhitelist(self, line):
        with open(sWhiteListFileName, 'r') as f:
            for sLineInFile in f:
                sLineInFile = sLineInFile.strip()
                print(sLineInFile)
        print("...")
        return

    def help_addToWhitelist(self):
        print '\n'.join([ 'addToWhitelist [52.19.24.61/32 # DARKGRIFTER]',
                           'Add an entry to the Whitelist',
                           ''])

    def do_addToWhitelist(self, line):
        print("line: " + str(line))
        with open(sWhiteListFileName, "a") as myfile:
            myfile.write("\n")
            myfile.write(line)
        cleanUpFile(sWhiteListFileName)
        print("---")
        return

    # --- --- --- #

    def help_showGraylist(self):
        print '\n'.join([ 'showGraylist',
                           'List the Current Graylist',
                           ])

    def do_showGraylist(self, line):
        with open(sGrayListFileName, 'r') as f:
            for sLineInFile in f:
                sLineInFile = sLineInFile.strip()
                print(sLineInFile)
        print("...")
        return

    def help_addToGraylist(self):
        print '\n'.join([ 'addToGraylist [52.19.24.61/32 # DARKGRIFTER]',
                           'Add an entry to the Graylist',
                           ''])

    def do_addToGraylist(self, line):
        print("line: " + str(line))
        with open(sGrayListFileName, "a") as myfile:
            myfile.write("\n")
            myfile.write(line)
        cleanUpFile(sGrayListFileName)
        print("---")
        return

    # --- --- --- #

    def help_listProjects(self):
        print '\n'.join([ 'listProjects',
                           'List the Current Projects',
                           ])

    def do_listProjects(self, line):
        with open('targets.txt', 'r') as f:
            for sLineInFile in f:
                sLineInFile = sLineInFile.strip()
                lLineInFile = sLineInFile.split(',')
                sProjectName = lLineInFile[0]
                sDomainName = lLineInFile[1]
                print(sProjectName + " \t " + sDomainName)
        print("...")
        return

    # --- --- --- #

    def help_addTarget(self):
        print '\n'.join([ 'addTarget [DINOEAGLE,dinoeagle.com,rootDomain]',
                          'addTarget [DINOEAGLE,8.8.8.8,ipAddy]',
                          'addTarget [DINOEAGLE,8.8.8.0/24,netBlock]',
                           'Add a Target to a Project',
                           ''])

    def do_addTarget(self, line):
        print("line: " + str(line))
        with open("targets.txt", "a") as myfile:
            myfile.write("\n")
            myfile.write(line)
        print("...")
        return

    # --- --- --- #

    def help_autoPilot(self):
        print '\n'.join([ 'autoPilot',
                           'Input Root Domain Name and Watch DarkTools Take Off!',
                           ])

    def do_autoPilot(self, line):
        print str(line)
        sProject = line.strip()
        do_work_son(sProject)
        print "... Batch Successfully Sent!"
        return

    def help_banner(self):
        print '\n'.join([ 'banner',
                           'Displays that sweet banner',
                           ])

    def do_banner(self, line):
        """display the banner"""
        print banner_Str

    # --- --- --- #

    def help_setAutoPilotInterval(self):
        print '\n'.join([ 'setAutoPilotInterval [86400]',
                           'Set the AutoPilot Interval to Every 4 Hours',
                           ''])

    def do_setAutoPilotInterval(self, line):
        print("line: " + str(line))
        os.remove("autopilot_interval.txt")
        with open("autopilot_interval.txt", "w") as myfile:
            myfile.write(line)
        print("---")
        return

    # --- --- --- #

    def do_EOF(self, line):
        """exit the console"""
        return True

    def do_exit(self, line):
        """exit the console"""
        return True

    def do_quit(self, line):
        """exit the console"""
        return True

    # --- --- --- #

if __name__ == '__main__':
    print banner_Str
    myDarkToolsWorld = DarkToolsWorld()
    myDarkToolsWorld.prompt = 'DARKTOOLS> '
    myDarkToolsWorld.cmdloop('Starting DARKTOOLS...')