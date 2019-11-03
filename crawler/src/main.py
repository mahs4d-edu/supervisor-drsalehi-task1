import os
import time
import pika

from crawler import Crawler


# load constants from environment variables
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
api_id = os.getenv('TELECRAWL_API_ID', 28800)
api_hash = os.getenv('TELECRAWL_API_HASH', 'b723b335c560c0897a0bdf4d5d77bba1')
session = '/data/telecrawl/sessions/session'

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

# create the crawler from loaded constants
print('setting up crawler ...')
crawler = Crawler(session, api_id, api_hash, rabbitmq_channel)

# start crawling ...
print('starting crawler ...')
crawler.start()
