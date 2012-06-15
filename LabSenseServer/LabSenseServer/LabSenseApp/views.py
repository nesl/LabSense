from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Channel, Measurement

def index(request):
    c = {}
    c['channels']= Channel.objects.all()
    return render_to_response("index.html", c, context_instance=RequestContext(request))

def channel(request, channel):
    c = {}
    c['channels']= Channel.objects.all()
    current_channel = Channel.objects.filter(slug=channel)[0]
    c['current_channel'] = current_channel
    c['sensors'] = [i + 1 for i in range(current_channel.num_sensors)]
    return render_to_response("channel.js", c, context_instance=RequestContext(request))
