import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    groups = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to the group
        await self.send_group(message)

    async def send_group(self, message):
        await self.send(text_data=json.dumps({"message": message}))

    async def create_group(self, group_name):
        self.groups.append(group_name)
