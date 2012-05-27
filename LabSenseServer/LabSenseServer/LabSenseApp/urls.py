from django.conf.urls.defaults import *

urlpatterns = patterns('LabSenseApp.views',
    (r'^$', 'index'),

    (r'^(?P<channel>\w+)/$', 'channel')
)
