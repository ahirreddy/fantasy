from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^fantasy/', include('fantasy.urls')),
)