import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection"""
        try:
            # Check if user is authenticated
            if self.scope["user"].is_authenticated:
                self.user = self.scope["user"]
                self.room_group_name = f"user_{self.user.id}"

                # Join room group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()

                # Send connection confirmation
                await self.send(text_data=json.dumps({
                    'type': 'connection_established',
                    'message': 'Connected to game channel'
                }))
            else:
                # Reject connection for unauthenticated users
                await self.close()
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'room_group_name'):
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle WebSocket messages from client"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'message')
            
            if message_type == 'ping':
                # Respond to ping with pong
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'message': 'pong'
                }))
            
        except json.JSONDecodeError as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def game_result(self, event):
        """Handle game result messages"""
        message = event['message']
        
        # Send game result to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_result',
            'data': message
        })) 