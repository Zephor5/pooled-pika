mypika
======

.. image:: https://img.shields.io/pypi/v/pooled-pika.svg
   :target: https://pypi.python.org/pypi/pooled-pika
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/pooled-pika.svg
   :target: https://pypi.python.org/pypi/pooled-pika
   :alt: PyPI Monthly downloads

.. image:: https://img.shields.io/travis/Zephor5/pooled-pika/master.svg
   :target: http://travis-ci.org/Zephor5/pooled-pika
   :alt: Build Status

a connection pool wrapper about async pika, using twisted TODO tornado and so on

Notice
------
just support twisted connection now

Usage
-----
sample:

.. code :: python

    # with connection
    from pika import URLParameters
    from pooled_pika import PooledConn

    AMQP_PARAM = URLParameters('amqp://user:pwd@amqpserver')
    pooled_conn = PooledConn(AMQP_PARAM)
    d = pooled_conn.acquire()
    d.addCallbacks(_on_conn, _on_err_conn) # you will get a TwistedProtocolConnection object
    d.addErrback(_on_err)
    d.addBoth(pooled_conn.release)  # must release what acquired anyway

or:

.. code :: python

    # with channel
    from pika import URLParameters
    from pooled_pika import PooledConn

    AMQP_PARAM = URLParameters('amqp://user:pwd@amqpserver')
    pooled_conn = PooledConn(AMQP_PARAM)
    d = pooled_conn.acquire(channel=True)
    d.addCallbacks(_on_channel, _on_err_channel) # you will get a TwistedChannel object
    d.addErrback(_on_err)
    d.addBoth(pooled_conn.release)  # must release what acquired anyway
