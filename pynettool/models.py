import logging

import jnettool.tools.elements.NetworkElement


class NetworkElement(object):
    def __init__(self, ip):
        self._ne = jnettool.tools.elements.NetworkElement(ip)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ne.cleanup('commit')
        self._ne.disconnect()

    @property
    def routing_table(self):
        try:
            return RoutingTable(self._ne.getRoutingTable())
        except jnettool.tools.elements.MissingVar:
            logging.exception('No routing table found')
            self._ne.cleanup('rollback')
            return RoutingTable()


class RoutingTable(list):
    def __init__(self, routing_table=None):
        self._rt = routing_table
        routes = [Route(self._rt.getRouteByIndex(RToffset)) for RToffset in range(self._rt.getSize())] \
            if self._rt else []
        super(RoutingTable, self).__init__(routes)


class Route(object):
    def __init__(self, route):
        self._route = route

    @property
    def name(self):
        return self._route.getName()

    @property
    def ip_addr(self):
        return self._route.getIpAddr()
