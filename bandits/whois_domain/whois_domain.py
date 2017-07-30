from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son(sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService):
    getToLogging()
    try:
        import pythonwhois
        logging.debug("whois_domain() sTarget: " + str(sDomain))
        domain_whois = pythonwhois.net.get_whois_raw(sDomain)
        logging.debug("whois_domain() domain_whois: " + str(domain_whois))
        sSourceTool = 'whois_domain'
        #
        sCmdOut = str(domain_whois)
        logging.debug("sCmdOut: " + str(sCmdOut))
        #
        sSeverity = "INFO"
        jEvent = {
            "project": sProject,
            "uniq_selector_id": sUniqSelectorId,
            "uniq_target_id": sUniqTargetId,
            "domain": sDomain,
            "whois_domain": sCmdOut,
            "severity": sSeverity
        }
        splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("domainname_whois() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


'''
micro service
'''

class WhoisDomain:
    """ Event listening service. """
    name = "whois_domain"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("whois_domain received:", payload)

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