import pynettool.tools.elements.NetworkElement
import pynettool.tools.Routing
import pynettool.tools.RouteInspector


ne = pynettool.tools.elements.NetworkElement('171.0.2.45')
try:
    routing_table = ne.getRoutingTable()
except pynettool.tools.elements.MissingVar:
    logging.exception('No routing table found')
    ne.cleanup('rollback')
else:
    num_routes = routing_table.getSize()
    for RToffset in range(num_routes):
        route = routing_table.getRouteByIndex(RToffset)
        name = route.getName()
        ipaddr = route.getIPAddr()
        print "%15s -> %s" % (name, ipaddr)
finally:
    ne.cleanup('commit')
    ne.disconnect()
