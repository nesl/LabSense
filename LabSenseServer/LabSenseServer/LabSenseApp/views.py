from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    c = {}
    c = RequestContext(request, c)
    return render_to_response("index.html", c)

def raritan(request):
    c = {'channel': 'raritan'}
    c = RequestContext(request, c)
    return render_to_response("raritan.html", c)

def veris(request):
    c = {}
    c = RequestContext(request, c)
    return render_to_response("generic_channel.html", c)

def zwave(request):
    c = {}
    c = RequestContext(request, c)
    return render_to_response("generic_channel.html", c)
