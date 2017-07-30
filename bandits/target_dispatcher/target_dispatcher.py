from nameko.events import BROADCAST, event_handler
from sharingthelove import *

class TargetDispatcher:
    """ Event listening service. """
    name = "target_dispatcher"

    @event_handler("smokey", "event_type", handler_type=BROADCAST, reliable_delivery=False)
    def handle_event(self, payload):
        dTarget = payload
        #
        sProject = dTarget["project"]
        sUniqSelectorId = dTarget["uniq_selector_id"]
        sUniqTargetId = dTarget["uniq_target_id"]
        sDomain = dTarget["domain"]
        sIp = dTarget["ip"]
        sProtocol = dTarget["protocol"]
        sOpenTcpPort = dTarget["port"]
        sTcpService = dTarget["service"]
        #
        jEvent = {
            "project": sProject,
            "uniq_selector_id": sUniqSelectorId,
            "uniq_target_id": sUniqTargetId,
            "domain": sDomain,
            "ip": sIp,
            "protocol": sProtocol,
            "port": sOpenTcpPort,
            "service": sTcpService,
            "selectortype": "target",
            "severity": "INFO"
        }
        sSourceTool = "target_dispatcher"
        splunkEvent(jEvent, sSourceTool)
        print("service target_dispatcher received:", payload)
