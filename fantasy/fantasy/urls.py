from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from fantasy import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^teams/', views.team_average, name='team_average'),
    url(r'^team_average/', views.team_player_average_total, name='team_player_average_total'),
    url(r'^on_team_average/', views.team_player_average_total_on_team, name='team_player_average_total_on_team'),
    # Examples:
    # url(r'^$', 'fantasy.views.home', name='home'),
    # url(r'^fantasy/', include('fantasy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
