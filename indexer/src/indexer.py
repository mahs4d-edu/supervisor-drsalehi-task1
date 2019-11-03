class Indexer:
    def __init__(self, es):
        self.es = es

    def setup(self):
        """
        creates index on elasticsearch
        """
        schema = {
            "mappings": {
                "properties": {
                    "sender": {
                        "type": "text"  # formerly "string"
                    },
                    "text": {
                        "type": "text"
                    },
                }
            }
        }

        self.es.indices.create(index='telecrawl_message',
                               body=schema, ignore=400)

    def on_message(self, sender, text):
        """
        indexes the message into elasticsearch
        """
        print("Indexing > {0}: {1}".format(sender, text))
        body = {
            'sender': sender,
            'text': text,
        }
        self.es.index(index='telecrawl_message', body=body)
