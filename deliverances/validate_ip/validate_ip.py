import argparse

from nameko.rpc import rpc

from sharingthelove import *

from netaddr import IPNetwork, IPAddress

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def validate_ip(sProject, sTarget, lBlackList, lWhiteList, lGrayList):
    fGoodToGo = False
    #
    getToLogging()
    #
    sSourceTool = 'validate_ip'
    sSeverity = 'INFO'
    #
    sIpAddy = sTarget.strip()
    fOnTheBlackList = False
    fOnTheWhiteList = False
    fOnTheGrayList = False
    fOnTheSelectorList = False
    #
    sCidr = 'unknown'
    sCidrDesc = 'unknown'
    sList = 'unknownlist'
    sState = 'unknown'
    #
    if 0 <= len(lBlackList):
        # BlackList is known bad IP ranges like the DoD or private ip blocks
        for sLineInBlackList in lBlackList:
            (sBlackListCidr, sBlackListDescription) = sLineInBlackList.split('#')

            sBlackListCidr = sBlackListCidr.strip()
            logging.debug("sBlackListCidr: " + sBlackListCidr)

            sBlackListDescription = sBlackListDescription.strip()
            logging.debug("sBlackListDescription: " + sBlackListDescription)

            if IPAddress(sIpAddy) in IPNetwork(sBlackListCidr):
                logging.info( "Ip in Network Range for Blacklist! " + sIpAddy + " in " + sBlackListCidr )
                fOnTheBlackList = True
                sCidr = sBlackListCidr
                sCidrDesc = sBlackListDescription
                sList = 'blacklist'
                sState = 'intheblacklist'
                fGoodToGo = False
            else:
                logging.info( "Ip NOT in Network Range for Blacklist! " + sIpAddy + " in " + sBlackListCidr )
    else:
        logging.error("No items within the lBlackList: " + lBlackList)
        fGoodToGo = False # ERROR no list!

    if fGoodToGo == False:
        # WhiteList is known good IP ranges like known datacenters
        if 0 <= len(lWhiteList):
            for sLineInWhiteList in lWhiteList:
                (sWhiteListCidr, sWhiteListDescription) = sLineInWhiteList.split('#')

                sWhiteListCidr = sWhiteListCidr.strip()
                logging.debug("sWhiteListCidr: " + sWhiteListCidr)

                sWhiteListDescription = sWhiteListDescription.strip()
                logging.debug("sWhiteListDescription: " + sWhiteListDescription)

                if IPAddress(sIpAddy) in IPNetwork(sWhiteListCidr):
                    logging.info("Ip in Network Range for Whitelist! " + sIpAddy + " in " + sWhiteListCidr)
                    fOnTheWhiteList = True
                    sCidr = sWhiteListCidr
                    sCidrDesc = sWhiteListDescription
                    sList = 'whitelist'
                    sState = 'inthewhitelist'
                    fGoodToGo = True
                else:
                    logging.info("Ip NOT in Network Range for Whitelist! " + sIpAddy + " in " + sWhiteListCidr)
        else:
            logging.error("No items within the lWhiteList: " + lWhiteList)
            fGoodToGo = False  # ERROR no list!

    if fGoodToGo == False:
        # GrayList is known and popular cloud providers (AWS & AZURE)
        if 0 <= len(lGrayList):
            for sLineInGrayList in lGrayList:
                (sGrayListCidr, sGrayListDescription) = sLineInGrayList.split('#')

                sGrayListCidr = sGrayListCidr.strip()
                logging.debug("sGrayListCidr: " + sGrayListCidr)

                sGrayListDescription = sGrayListDescription.strip()
                logging.debug("sGrayListDescription: " + sGrayListDescription)

                if IPAddress(sIpAddy) in IPNetwork(sGrayListCidr):
                    logging.info("Ip in Network Range for Graylist! " + sIpAddy + " in " + sGrayListCidr)
                    fOnTheGrayList = True
                    sCidr = sGrayListCidr
                    sCidrDesc = sGrayListDescription
                    sList = 'graylist'
                    sState = 'inthegraylist'
                    fGoodToGo = True
                else:
                    logging.info("Ip NOT in Network Range for Graylist! " + sIpAddy + " in " + sGrayListCidr)
        else:
            logging.error("No items within the lGrayList: " + lGrayList)
            fGoodToGo = False  # ERROR no list!
    #
    jEvent = {
        "project": sProject,
        "dest": sIpAddy,
        "cidr": sCidr,
        "cidr_desc": sCidrDesc,
        "list": sList,
        "state": sState,
        "severity": sSeverity
    }
    splunkEvent(jEvent, sSourceTool)
    #
    return fGoodToGo

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class ValidateIp:
    name = "service_validate_ip"

    @rpc
    def remote_method(self, sProject, sTarget, lBlackList, lWhiteList, lGrayList):
        return validate_ip(sProject, sTarget, lBlackList, lWhiteList, lGrayList)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
standalone 
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a")  # project name
    parser.add_argument("-b")  # target ip
    parser.add_argument("-c")  # project name
    parser.add_argument("-d")  # target ip
    parser.add_argument("-e")  # project name
    args, leftovers = parser.parse_known_args()
    if args.a is not None:
        print "a has been set (value is %s)" % args.a
        print "b has been set (value is %s)" % args.b
        print "a has been set (value is %s)" % args.c
        print "b has been set (value is %s)" % args.d
        print "a has been set (value is %s)" % args.e
        fValid = validate_ip(args.a, args.b, args.c, args.d, args.e)
        print("fValid: " + str(fValid))

main()