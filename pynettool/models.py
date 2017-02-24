import jnettool.tools.elements.NetworkElement


class NetworkElement(object):
    def __init__(self, ip):
        self._ne = jnettool.tools.elements.NetworkElement(ip)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ne.cleanup('commit')
        self._ne.disconnect()
