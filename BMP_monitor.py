#!/usr/bin/python
from twisted.internet import protocol, reactor
import struct
from core.factory import BMPFactory
from core.protocol import BMP
from handler.default import DefaultHandler
import logging








if __name__ == '__main__':
    LOG = logging.getLogger(__name__)



    handler = DefaultHandler()
    handler.init()

    reactor.listenTCP(5000, BMPFactory(handler=handler))
    reactor.run()