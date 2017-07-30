from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

from ftplib import FTP, error_perm

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    try:
        sNameOfFunction = 'anon_ftp'
        if ("ftp" == sTcpService):
            logging.debug("sTcpService: " + str(sTcpService))
            logging.debug("sOpenTcpPort: " + str(sOpenTcpPort))
            try:
                oFtp = FTP()
                oFtp.connect(sIp, int(sOpenTcpPort))
                sLoginResult = oFtp.login("anonymous", "anon@example.com")
                if ("Login successful" in sLoginResult):
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
                        "bandit_result": "Anonymous FTP w/ username: anonymous and password: anon@example.com worked!"
                    }
                    splunkEvent(jEvent, sNameOfFunction)  # sSourceTool = sNameOfFunction
                oFtp.close()
            except Exception as e:
                logging.error("traceback.format_exc(): " + traceback.format_exc())
                logging.error("str(Exception): " + str(e))
                logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class AnonFtp:
    """ Event listening service. """
    name = "anon_ftp"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("service " + str(self.name) + " received:" + str(payload))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''

standalone

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