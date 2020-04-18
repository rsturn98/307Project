from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import models, game
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['author']
        action = text_data_json['action']
        room_name = self.room_group_name
        print(action)
        # let's make a thing to handle each action
        if action == "Chat":
            print("Chatting")
            update = "No"
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author': name,
                    'update': update
                }
            )
            await game.addChat(self.room_group_name, message, name)
        elif action == "Join":
            print("Joining")
            await game.joinGame(self.room_group_name, name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'message': message,
                    'author': name,
                    'update': 'No'
                }
            )
            await game.addChat(self.room_group_name, message, name)
        else:
            print("Something else")
            await game.actionHandler(room_name, action, name)
            checker = [False]
            await game.actionChecker(room_name, checker)
            print(checker[0])
            if checker[0]:
                print("Both Actions Good to Go!")
                await game.turn(room_name)
            
            gameState = []
            await game.getGame(room_name, gameState)
            print(gameState)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'attack',
                    'message': message,
                    'author': name,
                    'update': 'Yes',
                    'p1HP':gameState[0],
                    'p1Attack':gameState[1],
                    'p1Dodge':gameState[2],
                    'p2HP':gameState[3],
                    'p2Attack':gameState[4],
                    'p2Dodge':gameState[5]
                }
            )
            await game.addChat(self.room_group_name, message, name)
#
#        if action == "Dodge":
#            print("Dodging")
#
#            await game.actionHandler(room_name, action, name)
#            await self.channel_layer.group_send(
#                self.room_group_name,
#                {
#                    'type': 'dodge',
#                    'message': message,
#                    'author': name
#                }
#            )
#            await game.addChat(self.room_group_name, message, name)
#
#        if action == "Special":
#            print("Special")
#
#            await game.actionHandler(room_name, action, name)
#            await self.channel_layer.group_send(
#                self.room_group_name,
#                {
#                    'type': 'special',
#                    'message': message,
#                    'author': name
#                }
#            )
#            await game.addChat(self.room_group_name, message, name)
#        if action == "Power":
#            print("Powering Up")
#
#            await game.actionHandler(room_name, action, name)
#            await self.channel_layer.group_send(
#                self.room_group_name,
#                {
#                    'type': 'powerup',
#                    'message': message,
#                    'author': name
#                }
#            )
#            await game.addChat(self.room_group_name, message, name)
#        
#        if action == "Join":
#            print("Joining")
#            await game.joinGame(self.room_group_name, name)
#            await self.channel_layer.group_send(
#                self.room_group_name,
#                {
#                    'type': 'join',
#                    'message': message,
#                    'author': name
#                }
#            )
#            await game.addChat(self.room_group_name, message, name)
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Chat'
        }))
    
    async def attack(self, event):
        message = event['message']
        author = event['author']
        update = event['update']
        p1HP = event['p1HP']
        p1Attack = event['p1Attack']
        p1Dodge = event['p1Dodge']
        p2HP = event['p2HP']
        p2Attack = event['p2Attack']
        p2Dodge = event['p2Dodge']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Attack',
            'update': 'Yes',
            'p1HP':p1HP,
            'p1Attack':p1Attack,
            'p1Dodge':p1Dodge,
            'p2HP':p2HP,
            'p2Attack':p2Attack,
            'p2Dodge':p2Dodge
        }))
    async def dodge(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Dodge'
        }))
    
    async def special(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Special'
        }))
    
    async def powerup(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Powerup'
        }))
    
    async def join(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'action': 'Join'
        }))
    
