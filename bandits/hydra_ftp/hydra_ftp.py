from nameko.events import BROADCAST, event_handler
from sharingthelove import *
import random, string
import requests
import time

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    sNameOfFunction = 'hydra_ftp'
    #
    logging.debug(sNameOfFunction+"() START")
    logging.debug("sProject: " + str(sProject))
    logging.debug("sDomain: " + str(sDomain))
    logging.debug("sIp: " + str(sIp))
    logging.debug("sProtocol: " + str(sProtocol))
    logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
    logging.debug("sTcpService: " + str(sTcpService))
    #
    sSourceTool = sNameOfFunction
    #
    sUrl = None
    if ("ftp" == sTcpService):  # ftp
        logging.debug("sTcpService: " + str(sTcpService))
        logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
        try:
            sOutputFileName = getTimeMillSec() + "_output_" + sNameOfFunction + ".txt"
            sOutputFFP = '/opt/' + sOutputFileName
            #
            sCmdToExecute = 'hydra -L /opt/wordlists/top_shortlist_of_usernames.txt -P /opt/wordlists/top_shortlist_of_passwords.txt -f ' + sIp + ' '+sTcpService+' -V -s ' + sOpenTcpPort + ' -o ' + sOutputFFP
            logging.debug("sCmdToExecute: " + str(sCmdToExecute))
            lCmdToExecute = sCmdToExecute.split(" ")
            process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
            sCmdOut, sCmdErr = process.communicate()
            logging.debug("sCmdOut: " + str(sCmdOut))
            #
            try:
                iLineCount = 1
                with open(sOutputFFP, "r") as f:
                    for line in f:
                        if iLineCount > 1:
                            sCreds = line.strip()
                            jEvent = {
                                "project": sProject,
                                "uniq_selector_id": sUniqSelectorId,
                                "uniq_target_id": sUniqTargetId,
                                "domain": sDomain,
                                "ip": sIp,
                                "protocol": sProtocol,
                                "port": sOpenTcpPort,
                                "service": sTcpService,
                                "selector": sCreds,
                                "selectortype": "creds",
                                "severity": "INFO"
                            }
                            splunkEvent(jEvent, sSourceTool)
                        iLineCount = iLineCount + 1
            except Exception as e:
                logging.error("traceback.format_exc(): " + traceback.format_exc())
                logging.error("str(Exception): " + str(e))
                logging.error("testssl_sh() subprocess.Popen failed :\ ")
        except Exception as e:
            logging.error("traceback.format_exc(): " + traceback.format_exc())
            logging.error("str(Exception): " + str(e))
            logging.error(sNameOfFunction+"() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class HydraFtp:
    """ Event listening service. """
    name = "hydra_ftp"

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
