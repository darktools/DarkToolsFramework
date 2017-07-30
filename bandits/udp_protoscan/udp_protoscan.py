from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    try:
        sSourceTool = 'udp_protoscan'
        sIp = sIp.strip()
        sCmdToExecute = '/usr/bin/perl /opt/udp-proto-scanner/udp-proto-scanner.pl ' + sIp
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug(sSourceTool+"() sCmdOut: " + str(sCmdOut))
        #
        sSeverity = "INFO"
        #sTtl = "error_unknown"
        #sTime = "error_unknown"
        #sIp = "error_unknown"
        sIpStringToFind = 'Received reply to probe '
        lCmdOut = sCmdOut.splitlines()
        for sLine in lCmdOut:
            logging.debug("sLine: " + str(sLine))
            if sLine.find(sIpStringToFind) >= 0:
                sLine = sLine.strip()
                lSegaments = sLine.split()
                sProbeType = lSegaments[4]
                sPort = lSegaments[7]
                sPort = sPort[:-1]
                sHexReply = lSegaments[10]
                jEvent = {
                    "project": sProject,
                    "uniq_selector_id": sUniqSelectorId,
                    "uniq_target_id": sUniqTargetId,
                    "ip": sIp,
                    "dest": sIp,
                    "port": sPort,
                    "udp_probe": sProbeType,
                    "udp_response": sHexReply,
                    "severity": sSeverity
                }
                splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sSourceTool+"() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

class UdpProtoscan:
    """ Event listening service. """
    name = "udp_protoscan"

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