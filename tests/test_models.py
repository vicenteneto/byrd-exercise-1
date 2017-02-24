import unittest

from mock import patch, MagicMock


class TestNetworkElement(unittest.TestCase):
    def setUp(self):
        self.jnettool_mock = MagicMock()
        modules = {
            'jnettool': self.jnettool_mock,
            'jnettool.tools': self.jnettool_mock,
            'jnettool.tools.elements': self.jnettool_mock,
            'jnettool.tools.elements.NetworkElement': self.jnettool_mock,
            'jnettool.tools.elements.MissingVar': self.jnettool_mock
        }

        self.module_patcher = patch.dict('sys.modules', **modules)
        self.module_patcher.start()

        import pynettool
        self.pynettool = pynettool

    def tearDown(self):
        self.module_patcher.stop()

    @patch('jnettool.tools.elements.NetworkElement')
    def test_network_element_context(self, ne_mock):
        # Arrange
        ip = '171.0.2.45'
        ne_mock.return_value = MagicMock()

        # Act and Assert
        with self.pynettool.NetworkElement(ip) as ne:
            self.assertIsInstance(ne, self.pynettool.NetworkElement)

        ne_mock.assert_called_with(ip)

    @patch('jnettool.tools.elements.NetworkElement')
    def test_disconnect_network_element(self, ne_mock):
        # Arrange
        ip = '171.0.2.45'
        ne_mock.return_value = MagicMock()
        ne_mock.return_value.cleanup.return_value = MagicMock()
        ne_mock.return_value.disconnect.return_value = MagicMock()

        # Act
        with self.pynettool.NetworkElement(ip):
            pass

        # Assert
        ne_mock.return_value.cleanup.assert_called_with('commit')
        ne_mock.return_value.disconnect.assert_called_with()

    @patch('jnettool.tools.elements.NetworkElement')
    def test_raises_missing_var_on_get_routing_table(self, ne_mock):
        # Arrange
        ip = '171.0.2.45'
        ne_mock.return_value = MagicMock()
        ne_mock.return_value.getRoutingTable.side_effect = Exception()
        ne_mock.return_value.cleanup.return_value = MagicMock()

        # Act and Assert
        with self.pynettool.NetworkElement(ip) as ne:
            self.assertIsInstance(ne.routing_table, list)
            self.assertEqual(0, len(ne.routing_table))
            ne_mock.return_value.cleanup.assert_called_with('rollback')

    @patch('jnettool.tools.elements.NetworkElement')
    def test_get_routing_table(self, ne_mock):
        # Arrange
        ip = '171.0.2.45'
        route_ip = '127.0.0.1'
        route_name = 'Name'

        route_mock = MagicMock()
        route_mock.getName.return_value = route_name
        route_mock.getIpAddr.return_value = route_ip

        rt_mock = MagicMock()
        rt_mock.getSize.return_value = 1
        rt_mock.getRouteByIndex.return_value = route_mock

        ne_mock.return_value = MagicMock()
        ne_mock.return_value.getRoutingTable.return_value = rt_mock

        # Act and Assert
        with self.pynettool.NetworkElement(ip) as ne:
            self.assertEqual(1, len(ne.routing_table))

            route = ne.routing_table[0]
            self.assertEqual(route_name, route.name)
            self.assertEqual(route_ip, route.ip_addr)
