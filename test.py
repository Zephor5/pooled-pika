# coding=utf-8
import logging

from pika import URLParameters
from twisted.internet import defer
from twisted.internet import reactor
from twisted.trial.unittest import TestCase

from pooled_pika import PooledConn

__author__ = "zephor"

try:
    range = xrange
except NameError:
    pass

AMQP_PARAM = URLParameters("amqp://guest:guest@localhost:5672")


def sleep(_, seconds):
    d = defer.Deferred()
    reactor.callLater(seconds, d.callback, seconds)
    return d


class ConnTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pooled_conn = PooledConn(AMQP_PARAM,)

    def test_get_conn(self):
        self.n = 0
        test_d = []

        def plus(_c):
            self.n += 1
            return _c

        for i in range(100):
            d = self.pooled_conn.acquire(channel=True)
            d.addCallback(plus)
            d.addCallback(self.pooled_conn.release)
            d.addErrback(lambda err: logging.error(err))
            test_d.append(d)
        res_d = defer.DeferredList(test_d)
        res_d.addCallback(lambda _: self.assertEqual(self.n, 100))
        res_d.addCallback(lambda _: self.pooled_conn.clear())
        res_d.addCallback(sleep, 1)
        return res_d
