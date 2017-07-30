from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son(sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService):
    getToLogging()
    try:
        # ref: https://media.readthedocs.org/pdf/ipwhois/dev/ipwhois.pdf
        from ipwhois import IPWhois
        from pprint import pprint
        from ipwhois import IPDefinedError
        logging.debug("whois_ip() sIp: " + str(sIp))
        try:
            objIp_Whois = IPWhois(sIp)
            results = objIp_Whois.lookup_rdap(depth=1, inc_raw=True )
            logging.debug("whois_ip() results: " + str(results))
            jRawResults = results['raw']
            logging.debug("whois_ip() jRawResults: " + str(jRawResults))
        except IPDefinedError:
            logging.debug("whois_ip() Error: Private IP address, skipping IP!")
        sSourceTool = 'whois_ip'
        sSeverity = "INFO"
        jEvent = {
            "project": sProject,
            "uniq_selector_id": sUniqSelectorId,
            "uniq_target_id": sUniqTargetId,
            "ip": sIp,
            "whoisip": jRawResults,
            "severity": sSeverity
        }
        splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("ip_whois() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class WhoisIp:
    """ Event listening service. """
    name = "whois_ip"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("whois_ip received:", payload)

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