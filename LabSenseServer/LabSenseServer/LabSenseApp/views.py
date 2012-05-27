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
    c['current_channel'] = Channel.objects.filter(name=channel)[0]
    return render_to_response("raritan.html", c, context_instance=RequestContext(request))
