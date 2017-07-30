import argparse

from nameko.rpc import rpc

from sharingthelove import *

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

#  --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def find_tcp_service(sProject, sUniqSelectorId, sDomain, sIp, sOpenTcpPort):
    getToLogging()
    sSourceTool = 'service_scan'
    service_of_port = "unknown"
    version_of_service = "unknown"

    try:
        sCmdToExecute = '/usr/bin/nmap -Pn -n -sV -p ' + sOpenTcpPort + ' --reason ' + sIp
        lCmdToExecute = sCmdToExecute.split(" ")
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE)
        sCmdOut, sCmdErr = process.communicate()
        logging.debug("" + sSourceTool + "() sCmdOut: " + str(sCmdOut))
        sSeverity = "INFO"
    except Exception as e:
        logging.error("[ERROR] traceback.format_exc(): " + traceback.format_exc())
        logging.error("[ERROR] str(Exception): " + str(e))
        logging.error("" + sSourceTool + "() subprocess.Popen failed :\ ")

    try:
        for sCmdOutRow in sCmdOut.splitlines():
            logging.info("076 - output_cmdout_row: " + str(sCmdOutRow))
            sCmdOutRow = sCmdOutRow.strip()
            logging.info("078 - sOpenTcpPort: " + str(sOpenTcpPort))
            if sOpenTcpPort + '/tcp' in sCmdOutRow:
                try:
                    lCmdOutRow = sCmdOutRow.split()
                    logging.info(lCmdOutRow[1])
                    status_of_port = lCmdOutRow[1]
                    logging.debug("status_of_port: " + status_of_port)
                    service_of_port = lCmdOutRow[2]
                    logging.debug("service_of_port: " + service_of_port)
                    if "https" in service_of_port:
                        service_of_port = "https"
                    elif "ssl/http" in service_of_port:
                        service_of_port = "https"
                    elif "http" in service_of_port:
                        service_of_port = "http"
                    else:
                        service_of_port =  service_of_port.strip()
                    if service_of_port == 'tcpwrapped':
                        logging.debug("tcpwrapped -> service_of_port: " + service_of_port) # do nothing
                    else:
                        version_of_service = ", ".join(lCmdOutRow[3:])
                        logging.debug("version_of_service: " + version_of_service)
                        jEvent = {
                            "project": sProject,
                            "dest": sIp,
                            "port": sOpenTcpPort,
                            "state": status_of_port,
                            "service": service_of_port,
                            "uniq_selector_id": sUniqSelectorId,
                            "domain": sDomain,
                            "severity": sSeverity
                        }
                        splunkEvent(jEvent, sSourceTool)
                except:
                    logging.debug("[!] FAIL: spliting when found row with Pinging in it")
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("" + sSourceTool + "() subprocess.Popen failed :\ ")
    return service_of_port

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
micro service
'''

class ServiceReconFindTcpService:
    name = "service_recon_find_tcp_service"

    @rpc
    def remote_method(self, sProject, sUniqSelectorId, sDomain, sIp, sOpenTcpPort):
        return find_tcp_service(sProject, sUniqSelectorId, sDomain, sIp, sOpenTcpPort)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''
standalone

python gobuster_dirb.py -p EXAMPLE -d example.com -o 443 -s https

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
        oReturned = find_tcp_service(payload["project"], payload["uniq_selector_id"], payload["domain"], payload["ip"], payload["port"])
        print (str())
        print("END")

main()
