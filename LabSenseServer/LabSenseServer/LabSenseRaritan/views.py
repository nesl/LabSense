from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    #c = RequestContext(request, {})
    c = {}
    return render_to_response("socketio.html", c)
