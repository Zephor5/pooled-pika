mypika
======
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
