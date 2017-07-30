from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    try:
        sNameOfFunction = 'template_bandit'
        if ("http" == sTcpService or "https" == sTcpService):
            logging.debug("sTcpService: " + str(sTcpService))
            logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
            try:
                # Do Something Here Like This...
                sCmdToExecute = '/usr/bin/nmap -Pn -n -p '+sOpenTcpPort+' --script http-methods ' + sIp
                sCmdOut = runAndGetCmdOut( sCmdToExecute )
                lCmdOut = sCmdOut.splitlines()
                sIpStringToFind = 'Supported Methods'
                for sLine in lCmdOut:
                    logging.debug("sLine: " + str(sLine))
                    if sLine.find(sIpStringToFind) >= 0:
                        sLine = sLine.strip()
                        lSegaments = sLine.split(':')
                        sHttpMethods = lSegaments[1]
                        lHttpMethods = sHttpMethods.split()
                        for sResult in lHttpMethods:
                            # Whenever you have the result in a JSON like format, send it to Splunk using the splunkEvent() function! :)
                            jEvent = {
                                "project": sProject,
                                "uniq_selector_id": sUniqSelectorId,
                                "uniq_target_id": sUniqTargetId,
                                "domain": sDomain,
                                "ip": sIp,
                                "protocol": sProtocol,
                                "port": sOpenTcpPort,
                                "service": sTcpService,
                                "severity": "LOW",
                                "bandit": sNameOfFunction,
                                "bandit_status": "Successful",
                                "bandit_result": sResult
                            }
                            splunkEvent(jEvent, sNameOfFunction)  # sSourceTool = sNameOfFunction
            except Exception as e:
                logging.error("traceback.format_exc(): " + traceback.format_exc())
                logging.error("str(Exception): " + str(e))
                logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class TemplateBandit:
    """ Event listening service. """
    name = "template_bandit"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("service " + str(self.name) + " received:" + str(payload))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''

standalone - for quick development and testing

Example:

python something.py -a '{"project": "DINOEAGLE", "uniq_selector_id": "TEST003", "uniq_target_id": "TEST003", "domain":"www.dinoeagle.com", "ip": "52.213.140.175", "protocol": "tcp", "port": "443", "service": "https"}'

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