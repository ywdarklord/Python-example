from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^Users/', 'Users.views.uploadWithKeyAndCustomField', name='uploadWithKeyAndCustomField'),
    url(r'^returnpage/', 'returnpage.views.returnPage', name='returnPage'),
    url(r'^download/', 'download.views.download', name='download')

)
