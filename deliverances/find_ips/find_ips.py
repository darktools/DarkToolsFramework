import argparse

from nameko.rpc import rpc

from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def checkIfStringIsAnIpAddress(ip_Str):
    try:
        socket.inet_aton(ip_Str)
        # legal
        return True
    except socket.error:
        # Not legal
        return False

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def find_ips(sProject, sUniqSelectorId, sTarget):
    getToLogging()
    lIpAddresses = []
    sSeverity = "INFO"
    try:
        sSourceTool = 'all_ips'
        sCmdToExecute = "cpc_allips"
        #
        addrs_List = [str(i[4][0]) for i in socket.getaddrinfo(sTarget, 65535)]
        #ipv4addrs_List = []
        for item in addrs_List:
            if checkIfStringIsAnIpAddress(item):
                lIpAddresses.append(item)
        #
        sCmdOut = ",".join(lIpAddresses)
        logging.debug("sCmdOut: " + str(sCmdOut))
        #splunkTime(sProject, sSourceTool, sCmdToExecute, sCmdOut, "INFO", objSplunk)
    except:
        logging.error("all_ips() subprocess.Popen failed :\ ")
    lIpAddresses = sortUniqList(lIpAddresses)
    for sIP in lIpAddresses:
        jEvent = {
            "project": sProject,
            "uniq_selector_id": sUniqSelectorId,
            "selector": sIP,
            "selectortype": "ip",
            "domain": sTarget,
            "dest": sIP,
            "severity": sSeverity
        }
        splunkEvent(jEvent, sSourceTool)
    return lIpAddresses

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class ServiceReconFindIps:
    name = "service_recon_find_ips"

    @rpc
    def remote_method(self, sProject, sUniqSelectorId, sTarget):
        return find_ips(sProject, sUniqSelectorId, sTarget)

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
        lAllIpsNew = find_ips(args.a, args.b, args.c)
        print("lAllIpsNew: " + str(lAllIpsNew))

main()