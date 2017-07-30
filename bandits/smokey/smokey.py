from nameko.events import EventDispatcher, event_handler
from nameko.events import BROADCAST, event_handler
from nameko.rpc import rpc
import time

class Smokey:
    """ Event dispatching service. """
    name = "smokey"

    dispatch = EventDispatcher()

    @rpc
    def dispatching_method(self, payload):
        self.dispatch("event_type", payload)
        time.sleep(10) # not neeeded
        return "test" # not neeeded

