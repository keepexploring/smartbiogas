import re
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.generic.websockets import JsonWebsocketConsumer
import json
#from utilities import update_dashboard
log = logging.getLogger(__name__)
import pdb

from utilities import send_data

connections={'current_users':[]}
def connection_groups(**kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["dashboard"]

@channel_session_user_from_http
def ws_add_dashboard(message, **kwargs):
    """
    Perform things on connection start
    """
    # pdb.set_trace()
    
    user = message.user
    #groupName = 'test'
    Group("hellothere",channel_layer=message.channel_layer).add(message.reply_channel)
    #Group(groupName).add(Channel("abc"))
   # data = {'name':'andrew','uid':'asdasdsad','data':[1,2,3,45,5,4,6,4,3],'broken_biogas':22,'working_biogas':78}
   # Group("hellothere",channel_layer=message.channel_layer).send({"text": json.dumps(data)})
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []
    send_data()
    #update_dashboard(Group)
   #connections['current_users'].append({'reply_channel':message.reply_channel,"group":"hellothere","channel_layer":message.channel_layer})
    #pdb.set_trace()
   
 
def receive(content):
    """
    Called when a message is received with either text or bytes
    filled out.
    """
    channel_session_user = True
    http_user = True

@channel_session_user
def ws_disconnect_dashboard(message):
    """
    Perform things on connection close
    """
    Group("hellothere").discard(message.reply_channel)

@channel_session_user
def ws_message_dashboard(message):
   # pdb.set_trace()
    print("sending!!")
    print(message.content['text'])
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)


@channel_session
def msg_consumer_dashboard(message):
    # Save to model
    #room = message.content['room']
    #ChatMessage.objects.create(
   #     room=room,
    #    message=message.content['message'],
    #)
    # Broadcast to listening sockets
    #Group("chat-%s" % room).send({
    #    "text": message.content['message'],
   # })
    #pdb.set_trace()
   # data = {'name':'andrew','uid':'asdasdsad','data':[1,2,3,45,5,4,6,4,3],'broken_biogas':23,'working_biogas':45}
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)
    #Channel('update-data').send({"room": "test",
      #      "message": json.dumps(data)},immediately=True)

    


@channel_session_user_from_http
def ws_add_technicians(message, **kwargs):
    """
    Perform things on connection start
    """
    # pdb.set_trace()
    
    user = message.user
    #groupName = 'test'
    Group("hellothere",channel_layer=message.channel_layer).add(message.reply_channel)
    #Group(groupName).add(Channel("abc"))
    data = {'name':'andrew','uid':'asdasdsad','data':[1,2,3,45,5,4,6,4,3],'broken_biogas':22,'working_biogas':78}
    Group("hellothere",channel_layer=message.channel_layer).send({"text": json.dumps(data)})
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []
   
def receive(content):
    """
    Called when a message is received with either text or bytes
    filled out.
    """
    channel_session_user = True
    http_user = True

@channel_session_user
def ws_disconnect_technicians(message):
    """
    Perform things on connection close
    """
    Group("hellothere").discard(message.reply_channel)

@channel_session_user
def ws_message_technicians(message):
    print(message.content['text'])
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)


@channel_session
def msg_consumer_technicians(message):
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)



@channel_session_user_from_http
def ws_add_jobs(message, **kwargs):
    """
    Perform things on connection start
    """
    # pdb.set_trace()
    
    user = message.user
    #groupName = 'test'
    Group("hellothere",channel_layer=message.channel_layer).add(message.reply_channel)
    #Group(groupName).add(Channel("abc"))
    data = {'name':'andrew','uid':'asdasdsad','data':[1,2,3,45,5,4,6,4,3],'broken_biogas':22,'working_biogas':78}
    Group("hellothere",channel_layer=message.channel_layer).send({"text": json.dumps(data)})
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []
   
def receive(content):
    """
    Called when a message is received with either text or bytes
    filled out.
    """
    channel_session_user = True
    http_user = True

@channel_session_user
def ws_disconnect_jobs(message):
    """
    Perform things on connection close
    """
    Group("hellothere").discard(message.reply_channel)

@channel_session_user
def ws_message_jobs(message):
    print(message.content['text'])
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)


@channel_session
def msg_consumer_jobs(message):

    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)
   

@channel_session_user_from_http
def ws_add_biogas(message, **kwargs):
    """
    Perform things on connection start
    """
    # pdb.set_trace()
    
    user = message.user
    #groupName = 'test'
    Group("hellothere",channel_layer=message.channel_layer).add(message.reply_channel)
    #Group(groupName).add(Channel("abc"))
    data = {'name':'andrew','uid':'asdasdsad','data':[1,2,3,45,5,4,6,4,3],'broken_biogas':22,'working_biogas':78}
    Group("hellothere",channel_layer=message.channel_layer).send({"text": json.dumps(data)})
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []
   
def receive(content):
    """
    Called when a message is received with either text or bytes
    filled out.
    """
    channel_session_user = True
    http_user = True

@channel_session_user
def ws_disconnect_biogas(message):
    """
    Perform things on connection close
    """
    Group("hellothere").discard(message.reply_channel)

@channel_session_user
def ws_message_biogas(message):
    print(message.content['text'])
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)


@channel_session
def msg_consumer_biogas(message):
    Group('hellothere',channel_layer=message.channel_layer).send({"text": message.content['text']},immediately=True)
   