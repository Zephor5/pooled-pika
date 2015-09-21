# coding=utf-8

from pika.adapters import BaseConnection, TwistedProtocolConnection
from pika.connection import Parameters
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientCreator

__author__ = 'zephor'


class PoolIsFull(Exception):
    pass


class PooledConn(Deferred, object):
    """
    """

    __idle_pool = {}

    __using_pool = {}

    _my_params = {}
    _my_instances = {}

    max_size = 100

    retry = True

    timeout_conn = 1

    loop = reactor

    def __new__(cls, params, loop=None, timeout_conn=None, max_size=None, *args, **kwargs):
        """
        :param cls:
        :param params: connection params
        :param loop: loop to assign
        :param timeout_conn: connection timeout
        :param max_size: max pool size for each connection
        :param args:
        :param kwargs:
        :return: PoolConn instance
        """
        if isinstance(params, Parameters):
            _id = repr(params)
            instance = super(PooledConn, cls).__new__(cls)
            if _id in cls._my_params:
                # always update the params instance
                cls._my_params[_id] = params
            else:
                cls._my_params[_id] = params
                # only works when first created
                instance.max_size = max_size if max_size else cls.max_size
                instance.loop = loop if loop else cls.loop
                instance.timeout_conn = timeout_conn if timeout_conn > 0 else cls.timeout_conn
            # print 'new id', id(cls._my_params[_id])
            return instance
        else:
            raise TypeError('only accept pika Parameters type')

    def __init__(self, params, *args, **kwargs):
        """
        :param params:
        :param args: to keep with the __new__
        :param kwargs: to keep with the __new__
        :return:
        """
        self._params = params
        super(self.__class__, self).__init__(self)
        self.prepare()

    def __call__(self, conn=None):
        if isinstance(conn, BaseConnection):
            # print '__call__', conn
            _id = id(conn)
            if _id in self.__idle_pool:
                # conn is already idle pool
                pass
            elif _id in self.__using_pool:
                # put the conn back to idle
                self.__idle_pool[_id] = self.__using_pool.pop(_id)
            elif self.size < self.max_size:
                # add new conn in using pool
                self._conn = conn
                self.__using_pool[_id] = conn
            else:
                raise PoolIsFull()
            return conn
        elif hasattr(self, '_conn'):
            # print '__call__', 'recover'
            _id = id(self._conn)
            if _id in self.__using_pool:
                # put the conn back to idle
                self.__idle_pool[_id] = self.__using_pool.pop(_id)
            elif _id in self.__idle_pool:
                pass

    def __connect(self):
        params = self._params
        cc = ClientCreator(self.loop, TwistedProtocolConnection, params)
        _d = cc.connectTCP(params.host, params.port, timeout=self.timeout_conn)
        _d.addCallback(lambda p: p.ready)
        _d.addCallback(self)
        _d.chainDeferred(self)

    def prepare(self):
        """
        makes itself ready to work
        :return:
        """
        if self.__idle_pool:
            _id, conn = self.__idle_pool.popitem()
            self.__using_pool[_id] = conn
            self.addCallback(lambda c: c)
            self.loop.callLater(0, self.callback, conn)
        elif self.size == self.max_size:
            raise PoolIsFull()
        else:
            self.__connect()

    @property
    def size(self):
        return len(self.__idle_pool) + len(self.__using_pool)


if __name__ == '__main__':
    print PooledConn.__mro__
