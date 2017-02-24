"""
PyNetTool library
~~~~~~~~~~~~~~~~~

PyNetTool is a Python wrapper for the jnettool library.
"""

import logging

from .models import NetworkElement

__title__ = 'pynettool'
__author__ = 'Vicente Neto'

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
