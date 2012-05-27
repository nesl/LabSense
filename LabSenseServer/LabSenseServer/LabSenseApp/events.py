from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events

import time
import random

#from chat.models import ChatRoom
from LabSenseApp.models import Channel


#@events.on_message(channel="^room-")
@events.on_message(channel="^labsense")
def message(request, socket, context, message):
    """
    Event handler for a room receiving a message. First validates a
    joining user's name and sends them the list of users.
    """
    #channel = get_object_or_404(Channel, id=message["channel"])
    if message["action"] == "start":
        print "HELLO"
        time.sleep(1)
        i = random.randint(1,5)
        if(i == 1):
            socket.send({"action": "set", "current": 5, "time": 1})
        if(i == 2):
            socket.send({"action": "set", "current": 7, "time": 2})
        if(i == 3):
            socket.send({"action": "set", "current": 8, "time": 3})
        if(i == 4):
            socket.send({"action": "set", "current": 9, "time": 4})
        if(i == 5):
            socket.send({"action": "set", "current": 10, "time": 5})
        #time.sleep(1)
        #socket.send({"action": "set", "current": 6, "time": 2})
        #time.sleep(1)
        #socket.send({"action": "set", "current": 7, "time": 3})
        #time.sleep(1)
        #socket.send({"action": "set", "current": 8, "time": 4})
        #time.sleep(1)
        #socket.send({"action": "set", "current": 9, "time": 5})
        #name = strip_tags(message["name"])
        #user, created = room.users.get_or_create(name=name)
        #if not created:
            #socket.send({"action": "in-use"})
        #else:
            #context["user"] = user
            #users = [u.name for u in room.users.exclude(id=user.id)]
            #socket.send({"action": "started", "users": users})
            #user.session = socket.session.session_id
            #user.save()
            #joined = {"action": "join", "name": user.name, "id": user.id}
            #socket.send_and_broadcast_channel(joined)
    else:
        pass
        #try:
            #user = context["user"]
        #except KeyError:
            #return
        #if message["action"] == "message":
            #message["message"] = strip_tags(message["message"])
            #message["name"] = user.name
            #socket.send_and_broadcast_channel(message)






#@events.on_finish(channel="^room-")
@events.on_finish(channel="^labsense")
def finish(request, socket, context):
    """
    Event handler for a socket session ending in a room. Broadcast
    the user leaving and delete them from the DB.
    """
    try:
        user = context["user"]
    except KeyError:
        return
    left = {"action": "leave", "name": user.name, "id": user.id}
    socket.broadcast_channel(left)
    user.delete()
