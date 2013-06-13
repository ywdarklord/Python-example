from django.conf.urls import patterns, include, url
#from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^Users/', 'Users.views.uploadWithKeyAndCustomField', name='uploadWithKeyAndCustomField'),
    url(r'^returnpage/', 'returnpage.views.returnPage', name='returnPage'),

)
