from nameko.events import BROADCAST, event_handler
from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    sIp = sIp.strip()
    try:
        sSourceTool = 'traceroute_udp'
        sBinaryPath = "/usr/sbin/traceroute"
        sCmdToExecute = sBinaryPath + ' -U -p 53 ' + sIp
        #
        iMillis = int(round(time.time() * 1000))
        sMillis = str(iMillis)
        sUniq = sMillis + sProject + sIp
        #
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug(sSourceTool+"() sCmdOut: " + str(sCmdOut))
        #
        sSeverity = "INFO"
        sStringToFind = 'traceroute to'
        lCmdOut = sCmdOut.splitlines()
        for sLine in lCmdOut:
            logging.debug(sSourceTool+"() sLine: " + str(sLine))
            if sLine.find(sStringToFind) >= 0:
                logging.debug(sSourceTool+"() Skip")
            else:
                sLine = sLine.strip()
                lSegaments = sLine.split()
                sHopNum = lSegaments[0]
                sHopHostName = lSegaments[1]
                sHopIp = lSegaments[2]
                sHopIp = sHopIp[1:-1]
                logging.debug("sHopIp: " + sHopIp)
                sHopMs = lSegaments[3]
                jEvent = {
                    "project": sProject,
                    "uniq_selector_id": sUniqSelectorId,
                    "uniq_target_id": sUniqTargetId,
                    "dest_ip": sIp,
                    "traceroute_id": sUniq,
                    "hop_num": sHopNum,
                    "hop_host_name": sHopHostName,
                    "hop_ip": sHopIp,
                    "hop_ms": sHopMs,
                    "severity": sSeverity
                }
                splunkEvent(jEvent, sSourceTool)
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sSourceTool+"() subprocess.Popen failed :\ ")

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class TracerouteUdp:
    """ Event listening service. """
    name = "traceroute_udp"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son( payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"], payload["ip"], payload["protocol"], payload["port"], payload["service"] )
        print("traceroute_udp received:", payload)

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