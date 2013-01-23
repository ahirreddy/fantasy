from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from fantasy import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^all_players/', views.all_players, name='all_players'),
    url(r'^multiple_team_players/', views.multiple_team_players, name='multiple_team_players'),
    url(r'^team_average/', views.team_player_average_total, name='team_player_average_total'),
    url(r'^on_team_average/', views.team_player_average_total_on_team, name='team_player_average_total_on_team'),
    url(r'^per_minute_fpts/', views.per_minute_fpts, name='per_minute_fpts'),
    url(r'^per_position_rankings/', views.per_position_rankings, name='per_position_rankings'),
    url(r'^player_rankings/', views.player_rankings, name='player_rankings'),
    url(r'^individual_player/', views.individual_player, name='individual_player'),
    # Examples:
    # url(r'^$', 'fantasy.views.home', name='home'),
    # url(r'^fantasy/', include('fantasy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)