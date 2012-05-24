from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    c = RequestContext(request, {})
    return render_to_response("index.html", c)

def raritan(request):
    c = RequestContext(request, {})
    return render_to_response("generic_channel.html", c)

def veris(request):
    c = RequestContext(request, {})
    return render_to_response("generic_channel.html", c)

def zwave(request):
    c = RequestContext(request, {})
    return render_to_response("generic_channel.html", c)
