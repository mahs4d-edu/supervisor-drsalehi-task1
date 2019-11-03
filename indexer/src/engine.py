import json


class Engine:
    def __init__(self, rabbitmq_channel):
        self.rabbitmq_channel = rabbitmq_channel
        self.indexers = []

    def add_indexer(self, indexer):
        """
        adds the indexer to list of indexers active on this engine
        """
        self.indexers.append(indexer)

    def start(self):
        """
        starts the indexer engine by connecting to telecrawl_message channel of rabbitmq
        """
        self.rabbitmq_channel.queue_declare(queue='telecrawl_message')
        self.rabbitmq_channel.basic_consume(queue='telecrawl_message',
                                            auto_ack=True,
                                            on_message_callback=self._on_queue_event)
        self.rabbitmq_channel.start_consuming()

    def _on_queue_event(self, ch, method, properties, body):
        """
        translates the body of event and sends it to all indexers (1 by default)
        """
        payload = json.loads(body)
        for indexer in self.indexers:
            indexer.on_message(payload['sender'], payload['text'])
