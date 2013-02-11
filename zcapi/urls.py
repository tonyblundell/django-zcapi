from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('zcapi.views',
    url(r'^(?P<app>[0-9a-zA-Z]+)/(?P<model>[0-9a-zA-Z]+)/$', 'api'),
    url(r'^(?P<app>[0-9a-zA-Z]+)/(?P<model>[0-9a-zA-Z]+)/(?P<pk>\d+)/$', 'api'),
)