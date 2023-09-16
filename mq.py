#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pika, os, json
import random, string



def randomDigits(len=8):
    # letters = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(len))



def connParamsPrint(params):
    print("| Connection Paramters:")
    print("| blocked_connection_timeout", params.blocked_connection_timeout)
    print("| channel_max", params.channel_max)
    print("| heartbeat", params.heartbeat)
    print("| retry_delay", params.retry_delay)
    print("| socket_timeout", params.socket_timeout)
    print("| port", params.port)



def connSetup(cloudAMQP):
    # Parse CLODUAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL', cloudAMQP)
    params = pika.URLParameters(url)
    # print default connection parameters
    # connParamsPrint(params)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    return connection



def qSetup(connection, que):
    channel = connection.channel() # start a channel
    channel.queue_declare(queue=que) # Declare a queue
    return channel



def qSend(channel, que, msg):
    jsonMsg=json.dumps(msg)
    channel.basic_publish(exchange='',routing_key=que,
                          # set per-message TTL in milliseconds 
                          #properties=pika.BasicProperties(
                          #    expiration='60000',
                          #    ),
                          body=jsonMsg)
    # print("qSend:", que, jsonMsg)



def qReceive(channel, que):
    inMsg=""
    
    def process_function(msg):
        nonlocal inMsg
        inMsg=json.loads(msg)
        # print("qReceive Process:", que, inMsg)
        channel.stop_consuming()

    # create a function which is called on incoming messages
    def callback(ch, method, properties, body):
        # convert message to UTF-8
        body=body.decode()
        process_function(body)

    # print("qReceive", que)
    channel.basic_consume(que, callback, auto_ack=True)
    channel.start_consuming()
    return inMsg
