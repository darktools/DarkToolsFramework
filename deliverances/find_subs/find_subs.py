import argparse

from nameko.rpc import rpc

from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def theharvester_subdomains(sProject, sUniqSelectorId, sTarget):
    #getToLogging()
    lSubDomains = []
    lEmailAddys = []
    try:
        sSourceTool = 'theharvester_subdomains'
        sCmdToExecute = '/usr/bin/python /opt/theHarvester/theHarvester.py -d ' + sTarget + ' -b google'
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug("sCmdOut: " + str(sCmdOut))
    except Exception as e:
        logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
        logging.error("[ERROR] str(Exception): " + str(e))
        logging.error("gobuster_subdomains() subprocess.Popen failed :\ ")

    sSeverity = "INFO"
    lCmdLines = sCmdOut.splitlines()
    iLineCount = 1
    iEmailStart = 0
    iDomainStart = 0
    for sLineOut in lCmdLines:
        sLineOut = sLineOut.strip()
        logging.debug("sLineOut: " + str(sLineOut))
        if iLineCount is iEmailStart:
            if sLineOut is '':
                iEmailStart = 0
            else:
                if "No emails found" in sLineOut:
                    logging.debug("Skip - No emails found")
                else:
                    sEmailAddy = sLineOut
                    sEmailAddy = sEmailAddy.lower()
                    lEmailAddys.append(sEmailAddy)
                    logging.debug("append sLineOut: " + str(sEmailAddy))
                    jEvent = {
                        "project": sProject,
                        "uniq_selector_id": sUniqSelectorId,
                        "selector": sEmailAddy,
                        "selectortype": "email",
                        "severity": sSeverity
                    }
                    splunkEvent(jEvent, sSourceTool)
                iEmailStart = iEmailStart + 1
        elif iLineCount is iDomainStart:
            if sLineOut is '':
                iDomainStart = 0
            else:
                sLineOutNew = sLineOut.split(":")
                logging.debug("append sLineOutNew: " + str(sLineOutNew))
                sDomain = sLineOutNew[1]
                sDomain = sDomain.lower()
                lSubDomains.append(sDomain)
                logging.debug("append sDomain: " + str(sDomain))
                jEvent = {
                    "project": sProject,
                    "uniq_selector_id": sUniqSelectorId,
                    "selector": sDomain,
                    "selectortype": "domain",
                    "domaintype": "sub",
                    "severity": sSeverity
                }
                splunkEvent(jEvent, sSourceTool)
                iDomainStart = iDomainStart + 1
        else:
            if "[+] Emails found:" in sLineOut:
                iEmailStart = iLineCount + 2
                logging.debug("Emails found: iEmailStart: " + str(iEmailStart))
            if "[+] Hosts found in search engines:" in sLineOut:
                iDomainStart = iLineCount + 3
                logging.debug("Hosts found: iDomainStart: " + str(iDomainStart))
        iLineCount = iLineCount + 1
        logging.debug("END iLineCount: " + str(iLineCount))
    logging.debug("lSubDomains: " + str(lSubDomains))
    lSubDomains = sortUniqList(lSubDomains)
    lEmailAddys = sortUniqList(lEmailAddys)
    return (lSubDomains, lEmailAddys)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def gobuster_subdomains(sProject, sUniqSelectorId, sTarget):
    #getToLogging()
    logging.debug("gobuster_subdomains()")
    logging.debug("sProject: " + str(sProject))
    logging.debug("sTarget: " + str(sTarget))
    lSubDomains = []
    try:
        sSourceTool = 'gobuster_subdomains'
        sCmdToExecute = '/usr/bin/gobuster -m dns -u ' + sTarget + ' -i -fw -w /opt/wordlists/sort_uniq_knock_dnsrecon_fierce_recon-ng.txt'
        #sCmdToExecute = '/usr/bin/gobuster -m dns -u ' + sTarget + ' -i -fw -w /app/veryshortdnslist.txt'
        lCmdToExecute = sCmdToExecute.split(" ")
        logging.debug("sCmdToExecute: " + str(sCmdToExecute))
        logging.debug("lCmdToExecute: " + str(lCmdToExecute))
        logging.debug("Popen() START")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug("Popen() END")
        logging.debug("sCmdOut: " + str(sCmdOut))
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("gobuster_subdomains() subprocess.Popen failed :\ ")

    lCmdLines = sCmdOut.splitlines()
    for sLineOut in lCmdLines:
        sLineOut = sLineOut.strip()
        logging.debug("sLineOut: " + str(sLineOut))
        if "Found:" in sLineOut:
            lLineOut = sLineOut.split()
            sDomain = lLineOut[1]
            sDomain = sDomain.lower()
            logging.debug("lLineOut[1]: " + str(sDomain))
            lSubDomains.append(sDomain)
            jEvent = {
                "project": sProject,
                "uniq_selector_id": sUniqSelectorId,
                "selector": sDomain,
                "selectortype": "domain",
                "domaintype": "sub",
                "severity": "INFO"
            }
            splunkEvent(jEvent, sSourceTool)
    logging.debug("lSubDomains: " + str(lSubDomains))
    lSubDomains = sortUniqList(lSubDomains)
    return lSubDomains

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def find_subdomains(sProject, sUniqSelectorId, sRootDomain):
    getToLogging()
    sRootDomain = sRootDomain.strip()
    lAllDomains = []
    lAllDomains.append(sRootDomain)

    logging.debug("sProject: " + str(sProject))
    logging.debug("sTarget: " + str(sRootDomain))
    lSubDomainsFromTheHarvestor, lEmailsFromTheHarvestor = theharvester_subdomains(sProject, sUniqSelectorId, sRootDomain)
    lSubDomainsFromGoBuster = gobuster_subdomains(sProject, sUniqSelectorId, sRootDomain)

    lAllDomainsNew = lAllDomains + lSubDomainsFromTheHarvestor + lSubDomainsFromGoBuster
    lAllDomainsNew = sortUniqList(lAllDomainsNew)

    # res = u"{}-x".format(value)
    return lAllDomainsNew

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class ServiceReconFindSubs:
    name = "service_recon_find_subs"

    @rpc
    def remote_method(self, sProject, sUniqSelectorId, sRootDomain):
        return find_subdomains(sProject, sUniqSelectorId, sRootDomain)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
This is to debug indivdual issues with this service
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a")  # project name
    parser.add_argument("-b")  # project name
    parser.add_argument("-c")  # project name
    args, leftovers = parser.parse_known_args()
    if args.a is not None:
        print "a has been set (value is %s)" % args.a
        print "b has been set (value is %s)" % args.b
        print "c has been set (value is %s)" % args.c
        lAllDomainsNew = find_subdomains(args.a, args.b, args.c)
        print("lAllDomainsNew: " + str(lAllDomainsNew))

main()