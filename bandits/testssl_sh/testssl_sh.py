from nameko.events import BROADCAST, event_handler
from sharingthelove import *
from urlparse import urlparse

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    try:
        sNameOfFunction = 'testssl_sh'
        sUrl = None
        if ("https" == sTcpService) or ("ssl" in sTcpService) or ("tls" in sTcpService):  # ssl/https
            logging.debug("sTcpService: " + str(sTcpService))
            logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
            if sOpenTcpPort == "443":
                sUrl = 'https://' + sDomain
            else:
                sUrl = 'https://' + sDomain + ":" + sOpenTcpPort
            logging.debug("sUrl: " + str(sUrl))
            logging.info("[+] find resources on https")
            #
            try:
                sOutputFileName = getTimeMillSec() + "_output_" + sNameOfFunction + ".json"
                sOutputFFP = '/opt/' + sOutputFileName
                #
                sCmdToExecute = '/opt/testssl.sh/testssl.sh --jsonfile-pretty ' + sOutputFFP + ' ' + sUrl
                logging.debug("sCmdToExecute: " + str(sCmdToExecute))
                lCmdToExecute = sCmdToExecute.split(" ")
                process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
                sCmdOut, sCmdErr = process.communicate()
                logging.debug("sCmdOut: " + str(sCmdOut))

                # now process the output file and send to Splunk
                try:
                    file = open(sOutputFFP, "r")
                    sFileContents = file.read()
                    file.close()

                    logging.debug("type(sFileContents): " + str(type(sFileContents)))
                    logging.debug("sFileContents: " + str(sFileContents))

                    parse_object = urlparse(sUrl)
                    sScheme = parse_object.scheme
                    sNetloc = parse_object.netloc # Domain
                    sPath = parse_object.path  # /home/index.html

                    jEvent = {
                        "project": sProject,
                        "uniq_selector_id": sUniqSelectorId,
                        "uniq_target_id": sUniqTargetId,
                        "domain": sDomain,
                        "ip": sIp,
                        "protocol": sProtocol,
                        "port": sOpenTcpPort,
                        "service": sTcpService,
                        "severity": "INFO",
                        "selectortype": "url",
                        "scheme": sScheme,
                        "netloc": sNetloc,
                        "path": sPath,
                        "testssl_sh": sFileContents
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
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class TestsslSh:
    """ Event listening service. """
    name = "testssl_sh"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son( payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"], payload["ip"], payload["protocol"], payload["port"], payload["service"] )
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