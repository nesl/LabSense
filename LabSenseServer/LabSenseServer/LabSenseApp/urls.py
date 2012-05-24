from django.conf.urls.defaults import *

urlpatterns = patterns('LabSenseApp.views',
    (r'^$', 'index'),
    (r'^raritan/$', 'raritan'),
    (r'^zwave/$', 'zwave'),
    (r'^veris/$', 'veris'),
)
