from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^LabSense_Server/', include('LabSense_Server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    ("", include('django_socketio.urls')),
    (r'^$', include('LabSenseApp.urls')),
    (r'^raritan$', include('LabSenseRaritan.urls'))

)
