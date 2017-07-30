from nameko.events import BROADCAST, event_handler
from sharingthelove import *
import random, string
import requests

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    logging.debug("gobuster_dirb() START")
    logging.debug("sProject: " + str(sProject))
    logging.debug("sDomain: " + str(sDomain))
    logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
    logging.debug("sTcpService: " + str(sTcpService))
    lUrls = []
    fTooManyTwos = 0
    #
    sUrl = None
    if "https" == sTcpService:  # ssl/https
        logging.debug("sTcpService: " + str(sTcpService))
        logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
        if sOpenTcpPort == "443":
            sUrl = 'https://' + sDomain
        else:
            sUrl = 'https://' + sDomain + ":" + sOpenTcpPort
        logging.debug("sUrl: " + str(sUrl))
        logging.info("[+] find resources on https")
    elif "http" == sTcpService:
        logging.debug("sTcpService: " + str(sTcpService))
        logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
        if sOpenTcpPort == "80":
            sUrl = 'http://' + sDomain
        else:
            sUrl = 'http://' + sDomain + ":" + sOpenTcpPort
        logging.debug("sUrl: " + str(sUrl))
        logging.info("[+] find resources on http")
    #
    if sUrl is not None:
        try:
            iRandomLen = random.randint(7, 19)
            sRandomFilename = randomword(iRandomLen)
            rOne = requests.get(sUrl + '/' + sRandomFilename, verify=False)
            rOneStatus = rOne.status_code
            logging.debug("gobuster_dirb() rOneStatus: " + str(rOneStatus))
            #
            iRandomLen = random.randint(7, 19)
            sRandomFilename = randomword(iRandomLen)
            rTwo = requests.get(sUrl + '/' + sRandomFilename, verify=False)
            rTwoStatus = rTwo.status_code
            logging.debug("gobuster_dirb() rTwoStatus: " + str(rTwoStatus))
            #
            iRandomLen = random.randint(7, 19)
            sRandomFilename = randomword(iRandomLen)
            rThree = requests.get(sUrl + '/' + sRandomFilename, verify=False)
            rThreeStatus = rThree.status_code
            logging.debug("gobuster_dirb() rThreeStatus: " + str(rThreeStatus))
            #
            if (rOneStatus == 200) and (rTwoStatus == 200) and (rThreeStatus == 200):
                fTooManyTwos = 1
        except Exception as e:
            logging.error("traceback.format_exc(): " + traceback.format_exc())
            logging.error("str(Exception): " + str(e))
            logging.error("gobuster_subdomains() requests for 200 failed :\ ")

        if fTooManyTwos == 0:
            try:
                sSourceTool = 'gobuster_dirb'
                sCmdToExecute = '/usr/bin/gobuster -m dir -u ' + sUrl + ' -i -e -s 200,204 -w /opt/wordlists/quickhits_noslash.txt'
                logging.debug("sCmdToExecute: " + str(sCmdToExecute))
                lCmdToExecute = sCmdToExecute.split(" ")
                process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
                sCmdOut, sCmdErr = process.communicate()
                logging.debug("sCmdOut: " + str(sCmdOut))
            except Exception as e:
                logging.error("traceback.format_exc(): " + traceback.format_exc())
                logging.error("str(Exception): " + str(e))
                logging.error("gobuster_subdomains() subprocess.Popen failed :\ ")

            lCmdLines = sCmdOut.splitlines()
            for sLineOut in lCmdLines:
                sLineOut = sLineOut.strip()
                if "Status:" in sLineOut:
                    lLineOut = sLineOut.split()
                    sUrl = lLineOut[0]
                    sStatusCode = lLineOut[2]
                    sStatusCode = sStatusCode.split(")")
                    sStatusCode =  sStatusCode[0]
                    logging.debug("sStatusCode: " + str(sStatusCode))
                    lUrls.append(sUrl)

                    parse_object = urlparse(sUrl)
                    sDomain = parse_object.netloc
                    sPath = parse_object.path # /home/index.html
                    sProtocol = parse_object.scheme

                    jEvent = {
                        "project": sProject,
                        "uniq_selector_id": sUniqSelectorId,
                        "uniq_target_id": sUniqTargetId,
                        "selector": sUrl,
                        "statuscode": sStatusCode,
                        "domain": sDomain,
                        "path": sPath,
                        "protocol": sProtocol,
                        "selectortype": "url",
                        "severity": "INFO"
                    }
                    splunkEvent(jEvent, sSourceTool)
            logging.debug("lUrls: " + str(lUrls))
    return lUrls

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class GobusterDirb:
    """ Event listening service. """
    name = "gobuster_dirb"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("service " + str(self.name) + " received:" + str(payload))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''

standalone

python something.py -a '{"project": "DINOEAGLE", "uniq_selector_id": "TEST002124924zdwclzagzsjkqyykvsvxvvxtyjejcpzvr", "uniq_target_id": "TEST002529114cvftofiuobtotsdxsyucsmwupraskyixj", "domain":"www.dinoeagle.com", "ip": "52.213.140.175", "protocol": "tcp", "port": "443", "service": "https"}'

'''

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a")  # project name
    args, leftovers = parser.parse_known_args()
    if args.a is not None:
        print "a has been set (value is %s)" % args.a
        import ast
        payload = ast.literal_eval(str(args.a))
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("END")

main()

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #