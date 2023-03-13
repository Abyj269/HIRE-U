import json
from channels.consumer import AsyncConsumer
from channels.consumer import database_sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import User



class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected',event)
        user=self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept",
        })
            
    async def websocket_receive(self,event):
        print('receive',event)
        recieved_data=json.loads(event['text'])
        msg=recieved_data.get('message')
        if not msg:
            print('Error::empty message')
            return False
        sent_by_id=recieved_data.get('sent_by')
        send_to_id = recieved_data.get('sent_to')
        # if not msg:
        #     print('Error::empty message')
        #     return False
        
        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        if not sent_by_user:
            print('Error :: sent by user is incorrect')
        if not send_to_user:
                print('Error :: sent to user is incorrect')

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response ={
            'message':msg,
            'sent_by':self_user.id,
            'sent_to':send_to_id
            
        }

      
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(response)
        })

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat.message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat.message',
                'text': json.dumps(response)
            }
        )
        

    async def websocket_disconnect(self,event):
        print('disconnect',event)
    
    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
  

    @database_sync_to_async
    def get_user_object(self,user_id):
        qs=User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj=None
        return obj

    