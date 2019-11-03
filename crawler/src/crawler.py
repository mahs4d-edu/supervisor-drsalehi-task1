import os
import json
from telethon import TelegramClient, events, sync, utils


class Crawler:
    def __init__(self, session, api_id, api_hash, rabbitmq_channel):
        self.client = TelegramClient(session, api_id, api_hash)
        self.rabbitmq_channel = rabbitmq_channel

    def start(self):
        self.rabbitmq_channel.queue_declare('telecrawl_message')
        self.client.add_event_handler(self._on_message)
        self.client.start()

        # keep application alive during event listening
        try:
            print('(Press Ctrl+C to stop this)')
            self.client.run_until_disconnected()
        finally:
            self.client.disconnect()

    @events.register(events.NewMessage(incoming=True, outgoing=False))
    async def _on_message(self, event):
        sender = await event.get_sender()
        sender_name = utils.get_display_name(sender)
        message_text = event.text

        if message_text is not None and message_text != '':
            payload = {
                'text': message_text,
                'sender': sender_name
            }

            print('message from {0}: {1}'.format(
                payload['sender'], payload['text']))

            # publish the message to rabbitmq
            self.rabbitmq_channel.basic_publish(
                exchange='', routing_key='telecrawl_message', body=json.dumps(payload))
