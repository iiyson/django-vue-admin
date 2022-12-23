# -*- coding: utf-8 -*-
import urllib

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json
import dizhi1

from channels.layers import get_channel_layer
from jwt import InvalidSignatureError

from application import settings

send_dict = {}

# 发送消息结构体
def set_message(sender, msg_type, msg):
    text = {
        'sender': sender,
        'contentType': msg_type,
        'content': msg,
    }
    return text

#异步获取消息中心的目标用户
@database_sync_to_async
def _get_message_center_instance(message_id):
    from dvadmin.system.models import MessageCenter
    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list('target_user',flat=True)
    if _MessageCenter:
        return _MessageCenter
    else:
        return []

@database_sync_to_async
def _get_message_unread(user_id):
    from dvadmin.system.models import MessageCenterTargetUser
    count = MessageCenterTargetUser.objects.filter(users=user_id,is_read=False).count()
    return count or 0


def request_data(scope):
    query_string = scope.get('query_string', b'').decode('utf-8')
    qs = urllib.parse.parse_qs(query_string)
    return qs

class DvadminWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            import jwt
            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            decoded_result = jwt.decode(self.service_uid, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded_result:
                self.user_id = decoded_result.get('user_id')
                self.chat_group_name = "user_"+str(self.user_id)
                #收到连接时候处理，
                await self.channel_layer.group_add(
                    self.chat_group_name,
                    self.channel_name
                )
                await self.accept()
                # 发送连接成功
                await self.send_json(set_message('system', 'SYSTEM', '连接成功'))
                # 主动推送消息
                unread_count = await _get_message_unread(self.user_id)
                await self.send_json(set_message('system', 'TEXT', {"model":'message_center',"unread":unread_count}))
        except InvalidSignatureError:
            await self.disconnect(None)


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)
        print("连接关闭")
        await self.close(close_code)


class MegCenter(DvadminWebSocket):
    """
    消息中心
    """

    async def receive(self, text_data):
        # 接受客户端的信息，你处理的函数
        text_data_json = json.loads(text_data)
        message_id = text_data_json.get('message_id', None)
        user_list = await _get_message_center_instance(message_id)
        for send_user in user_list:
            await self.channel_layer.group_send(
                "user_" + str(send_user),
                {'type': 'push.message', 'json': text_data_json}
            )

    async def push_message(self, event):
        message = event['json']
        await self.send(text_data=json.dumps(message))


def websocket_push(user_id, message):
    """
    主动推送消息
    """
    username = "user_"+str(user_id)
    print(103,message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
    username,
    {
      "type": "push.message",
      "json": message
    }
    )


class realTimeChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_id']
        # self.room_group_name=self.room_name

        await self.channel_layer.group_add(self.room_name,self.channel_name )
        self.full_record_txt=''
        await self.accept()
        # await self.send(set_message('system', 'SYSTEM', '连接成功'))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name,self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # text_data是传入的json数据
        message = text_data
        message_asr = {}
        try:
            message_dict = json.loads(message)
            file_path = message_dict['wavPath']
            getasr = getAsr(file_path)
            text = getasr.getAsr_12123()
            print("转录：" + text)
            text = replace(text)
            print("去噪：" + text)

            record_data = ''
            if text != '':
                # print(text)
                texts = []
                for t in text:
                    texts.append(t)
                inputs = tokenizer(text, add_special_tokens=False, return_tensors="pt")
                with torch.no_grad():
                    logits = model(**inputs).logits
                predicted_token_class_ids = logits.argmax(-1)
                predicted_tokens_classes = [model.config.id2label[t.item()] for t in predicted_token_class_ids[0]]

                for index in range(len(predicted_tokens_classes)):
                    if predicted_tokens_classes[index] != 'O':
                        #                             if index > 1 or index < len(predicted_tokens_classes) - 1:
                        #                                 if
                        texts[index] = (texts[index] + predicted_tokens_classes[index]).replace('B-', '')
                for t in texts:
                    record_data = record_data + t
            print("断句：" + record_data)
            record_data = rule(record_data)
            print("标点处理：" + record_data)

            # 关键字提取
            self.full_record_txt += record_data
            keyInfo = dizhi1.extract(self.full_record_txt)
            # print(keyInfo)

            message_asr['text'] = record_data
            message_asr['date'] = message_dict['time']
            message_asr['mine'] = message_dict['identity']
            message_asr['name'] = message_dict['user']


            message_asr['img'] = '/static/img/profile.6d887530.jpg'
            message_asr['isTextarea'] = False
            message_asr['textarea'] = ''
            message_asr['isTag'] = False
            message_asr['tag'] = ['标签一', '标签二']
            message_asr['inputVisible'] = False
            message_asr['inputValue'] = ''

            chatData = list()
            chatData.append(message_asr)

            dictData = dict()
            dictData['useInfo'] = {'name': '刘亦菲', 'date': '5分05秒', 'phone': '15077559076'}
            dictData['chatData'] = chatData
            dictData['insertFormVal'] = {}
            dictData['keyFormVal'] = keyInfo
            print(dictData)

            dictData = json.dumps(dictData)
            # print(file_path)
        #                 if message:
        #                     time.sleep(2)
        except Exception as e:
            print(e)
        # 传到通道内
        else:
            await self.channel_layer.group_send(self.room_name,{'type':'chat_message','data':dictData})


    async def chat_message(self,event):
        message=event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message':message}))


# 测试用
# class realTimeChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name=self.scope['url_route']['kwargs']['room_name']
#         # self.room_group_name=self.room_name
#         self.record=''
#         await self.channel_layer.group_add(self.room_name,self.channel_name )
#         await self.accept()
#         # await self.send( '连接成功')
#
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_name,self.channel_name)
#
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_json=json.loads(text_data)
#         # self.record+=text_data_json['message']
#         self.record+=text_data_json['msg']
#         # 传到通道内
#         await self.channel_layer.group_send(self.room_name,{'type':'chat_message','message':self.record})
#
#
#     async def chat_message(self,event):
#         message=event['message']
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({'message':message}))