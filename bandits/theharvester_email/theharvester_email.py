from nameko.events import BROADCAST, event_handler
from sharingthelove import *
from nameko.rpc import rpc

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def do_work_son( sProject, sUniqSelectorId, sUniqTargetId, sDomain, sIp, sProtocol, sOpenTcpPort, sTcpService ):
    getToLogging()
    try:
        sNameOfFunction = 'theharvester_email'
        logging.debug("sDomain: " + str(sDomain))
        iCount = sDomain.count('.')
        #
        if iCount == 1:
            lDomain = sDomain.split('.')
            sSelector = lDomain[0]
        elif iCount == 2:
            lDomain = sDomain.rsplit('.', 2) # TODO: account for all TLDs including .co.uk type TLDs
            sSelector = lDomain[1]
        else:
            lDomain = sDomain.rsplit('.', 1) # TODO: account for all TLDs including .co.uk type TLDs
            sSelector = lDomain[0]
        logging.debug("sSelector: " + str(sSelector))
        #
        try:
            sSourceTool = 'theharvester_subdomains'
            sCmdToExecute = '/usr/bin/python /opt/theHarvester/theHarvester.py -d ' + sSelector + ' -b google'
            lCmdToExecute = sCmdToExecute.split(" ")
            process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
            sCmdOut, sCmdErr = process.communicate()
            logging.debug("sCmdOut: " + str(sCmdOut))
            #
            try:
                sSeverity = "INFO"
                lCmdLines = sCmdOut.splitlines()
                iLineCount = 1
                iEmailStart = 0
                iDomainStart = 0
                for sLineOut in lCmdLines:
                    sLineOut = sLineOut.strip()
                    logging.debug("sLineOut: " + str(sLineOut))
                    if iLineCount is iEmailStart:
                        if sLineOut is '':
                            iEmailStart = 0
                        else:
                            if "No emails found" in sLineOut:
                                logging.debug("Skip - No emails found")
                            else:
                                sEmailAddy = sLineOut
                                sEmailAddy = sEmailAddy.lower()
                                logging.debug("append sLineOut: " + str(sEmailAddy))
                                '''
                                jEvent = {
                                    "project": sProject,
                                    "uniq_selector_id": sUniqSelectorId,
                                    "selector": sEmailAddy,
                                    "selectortype": "email",
                                    "severity": sSeverity
                                }
                                splunkEvent(jEvent, sSourceTool)
                                '''
                                iCountEmailAddy = sEmailAddy.count('.')
                                if iCountEmailAddy < 1:
                                    sEmailAddy = sEmailAddy + ".com"

                                jEvent = {
                                    "project": sProject,
                                    "uniq_selector_id": sUniqSelectorId,
                                    "uniq_target_id": sUniqTargetId,
                                    "selector": sEmailAddy,
                                    "selectortype": "email",
                                    "severity": sSeverity
                                }
                                splunkEvent(jEvent, sNameOfFunction)  # sSourceTool = sNameOfFunction
                            iEmailStart = iEmailStart + 1
                    else:
                        if "[+] Emails found:" in sLineOut:
                            iEmailStart = iLineCount + 2
                            logging.debug("Emails found: iEmailStart: " + str(iEmailStart))
                    iLineCount = iLineCount + 1
                    logging.debug("END iLineCount: " + str(iLineCount))
            except Exception as e:
                logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
                logging.error("[ERROR] str(Exception): " + str(e))
                logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
        except Exception as e:
            logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
            logging.error("[ERROR] str(Exception): " + str(e))
            logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error(sNameOfFunction + "() subprocess.Popen failed :\ ")

####

class TheharvesterEmail:
    """ Event listening service. """
    name = "theharvester_email"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        print("service " + str(self.name) + " received:" + str(payload))

    @rpc
    def remote_method(self, payload):
        do_work_son(payload["project"], payload["uniq_selector_id"], payload["uniq_target_id"], payload["domain"],
                    payload["ip"], payload["protocol"], payload["port"], payload["service"])
        return "remote_method() returns"

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
