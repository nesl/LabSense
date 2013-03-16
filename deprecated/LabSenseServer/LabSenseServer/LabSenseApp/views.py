from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Channel, Measurement

def index(request):
    c = {}
    c['channels']= Channel.objects.all()
    return render_to_response("index.html", c, context_instance=RequestContext(request))

@login_required
def channel(request, channel):
    c = {}
    c['channels']= Channel.objects.all()
    current_channel = Channel.objects.filter(slug=channel)[0]
    c['current_channel'] = current_channel
    default_measurement = current_channel.measurement_set.all()[0].slug
    c['default_measurement'] = default_measurement
    c['sensors'] = [i + 1 for i in range(current_channel.num_sensors)]
    return render_to_response("channel.js", c, context_instance=RequestContext(request))

@login_required
def channel_measurement(request, channel, measurement):
    c = {}
    c['channels']= Channel.objects.all()
    current_channel = Channel.objects.filter(slug=channel)[0]
    c['current_channel'] = current_channel
    c['default_measurement'] = measurement
    c['sensors'] = [i + 1 for i in range(current_channel.num_sensors)]
    return render_to_response("channel.js", c, context_instance=RequestContext(request))
