import sys
import os
import time
import pika

from engine import Engine
from indexer import Indexer

# load constants
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
elasticsearch_host = os.getenv('ELASTICSEARCH_HOST')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT')

# connect to rabbitmq
print('initializing rabbitmq connection ...')
rabbitmq_connection = None
rabbitmq_channel = None
while True:
    try:
        rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_host, rabbitmq_port))
        rabbitmq_channel = rabbitmq_connection.channel()
        break
    except Exception:
        print('rabbitmq is not ready, trying again in 5 seconds')
        time.sleep(5)

# create Engine and Indexer and add the indexer to engine
print('setting up engine and indexer ...')
engine = Engine(rabbitmq_channel)
indexer = Indexer()

engine.add_indexer(indexer)

# start the engine
print('starting engine ...')
engine.start()
