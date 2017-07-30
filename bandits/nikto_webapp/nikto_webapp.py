from nameko.events import BROADCAST, event_handler
from sharingthelove import *
import random, string
import requests
import time

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    sNameOfFunction = 'nikto_webapp'
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
        logging.debug("sService: " + str(sTcpService))
        logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
        if sOpenTcpPort == "80":
            sUrl = 'http://' + sDomain
        else:
            sUrl = 'http://' + sDomain + ":" + sOpenTcpPort
        logging.debug("sUrl: " + str(sUrl))
        logging.info("[+] find resources on http")
    #
    if sUrl is not None:
        logging.debug("sTcpService: " + str(sTcpService))
        logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
        try:
            sOutputFileName = getTimeMillSec() + "_output_" + sNameOfFunction + ".txt"
            sOutputFFP = '/opt/' + sOutputFileName
            #
            sCmdToExecute = 'nikto -output ' + sOutputFFP + ' -h ' + sUrl
            #
            logging.debug("sCmdToExecute: " + str(sCmdToExecute))
            lCmdToExecute = sCmdToExecute.split(" ")
            process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
            sCmdOut, sCmdErr = process.communicate()
            logging.debug("sCmdOut: " + str(sCmdOut))
            #
            try:
                import csv
                import json

                csvfile = open('file.csv', 'r')
                jsonfile = open('file.json', 'w')

                fieldnames = ("Domain", "Ip", "Port", "OSVDB", "HTTP_Method", "Uri", "Description")
                reader = csv.DictReader(csvfile, fieldnames)
                iLineCount = 1
                for row in reader:
                    if iLineCount > 1:
                        json.dump(row, jsonfile)
                        jsonfile.write('\n')
                    iLineCount = iLineCount + 1

                # now process the output file and send to Splunk
                try:
                    file = open(jsonfile, "r")
                    sFileContents = file.read()
                    file.close()

                    jEvent = {
                        "project": sProject,
                        "uniq_selector_id": sUniqSelectorId,
                        "uniq_target_id": sUniqTargetId,
                        "domain": sDomain,
                        "ip": sIp,
                        "protocol": sProtocol,
                        "port": sOpenTcpPort,
                        "service": sTcpService,
                        "nikto_webapp": sFileContents,
                        "selector": sUrl,
                        "selectortype": "nikto_webapp",
                        "severity": "INFO"
                    }
                    splunkEvent(jEvent, sSourceTool)
                except Exception as e:
                    logging.error("traceback.format_exc(): " + traceback.format_exc())
                    logging.error("str(Exception): " + str(e))
                    logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
            except Exception as e:
                logging.error("traceback.format_exc(): " + traceback.format_exc())
                logging.error("str(Exception): " + str(e))
                logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
        except Exception as e:
            logging.error("traceback.format_exc(): " + traceback.format_exc())
            logging.error("str(Exception): " + str(e))
            logging.error(sNameOfFunction+"() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class NiktoWebapp:
    """ Event listening service. """
    name = "nikto_webapp"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son( payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"], payload["ip"], payload["protocol"], payload["port"], payload["service"] )
        print(self.name + " received:", payload)

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