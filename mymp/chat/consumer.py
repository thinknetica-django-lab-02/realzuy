import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.bot import reply_from_server
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': "Привет, чем могу помочь?",
                'datetime': timezone.now().isoformat(),
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': message,
                'datetime': timezone.now().isoformat(),
            }
        )

        reply_message = reply_from_server(message)
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': reply_message,
                'datetime': timezone.now().isoformat(),
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
