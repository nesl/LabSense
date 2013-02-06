from django.conf.urls.defaults import *

urlpatterns = patterns('LabSenseApp.views',
    (r'^$', 'index'),
    (r'^accounts/', include('accounts.urls')),

    (r'^(?P<channel>\w+)/$', 'channel'),
    (r'^(?P<channel>\w+)/(?P<measurement>\w+)$', 'channel_measurement')
)
