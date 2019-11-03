import sys
import os
import time
import pika
from elasticsearch import Elasticsearch

from engine import Engine
from indexer import Indexer

# load constants
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)
elasticsearch_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT', 9200)

rabbitmq_connection = None
rabbitmq_channel = None
es = None
engine = None


def setup_rabbitmq():
    global rabbitmq_connection
    global rabbitmq_channel

    # connect to rabbitmq
    print('initializing rabbitmq connection ...')
    while True:
        try:
            rabbitmq_connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitmq_host, rabbitmq_port))
            rabbitmq_channel = rabbitmq_connection.channel()
            break
        except Exception:
            print('rabbitmq is not ready, trying again in 5 seconds')
            if rabbitmq_connection is not None:
                rabbitmq_connection.sleep(5)
            else:
                time.sleep(5)


def setup_elasticsearch():
    global es

    # connect to elasticsearch
    print('initializing elasticsearch connection ...')
    while True:
        try:
            es = Elasticsearch(
                [{'host': elasticsearch_host, 'port': elasticsearch_port}])
            es.cluster.health(wait_for_status='yellow')
            break
        except Exception as ex:
            print(ex)
            print('elasticsearch is not ready, trying again in 5 seconds')
            rabbitmq_connection.sleep(5)


def setup_engine():
    global rabbitmq_connection
    global rabbitmq_channel
    global es
    global engine

    # create Engine and Indexer and add the indexer to engine
    print('setting up engine and indexer ...')
    engine = Engine(rabbitmq_channel)
    indexer = Indexer(es)

    engine.add_indexer(indexer)


def start_engine():
    global rabbitmq_connection
    global rabbitmq_channel
    global es
    global engine

    # start the engine
    setup_rabbitmq()
    setup_elasticsearch()
    setup_engine()
    print('starting engine ...')
    engine.start()

    try:
        rabbitmq_channel.start_consuming()
    except KeyboardInterrupt:
        rabbitmq_channel.stop_consuming()
        rabbitmq_connection.close()


start_engine()
