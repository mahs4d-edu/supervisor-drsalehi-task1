class Indexer:
    def __init__(self):
        pass

    def on_message(self, sender, text):
        print("Received from {0}: {1}".format(sender, text))
