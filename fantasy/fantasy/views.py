from django.http import HttpResponse
from fantasy.models import Fantasy
from django.shortcuts import render
from django_tables2 import RequestConfig
import django_tables2 as tables

class PlayerPointsTable(tables.Table):
  player_name = tables.Column(verbose_name="Player Name")
  avg_fpts = tables.Column(verbose_name="Avg Fpts")
  total_fpts = tables.Column(verbose_name="Total Fpts")
  games_played = tables.Column(verbose_name="Games Played")

  class Meta:
    attrs = {"class": "paleblue"}

class TeamAveragesTable(tables.Table):
  team_id = tables.Column(verbose_name="Team ID")
  team_avg = tables.Column(verbose_name="Team Avg")

  class Meta:
    attrs = {"class": "paleblue"}

def index(request):
  query = """SELECT player_name,
                    ROUND(AVG(fpts),2) as avg_fpts,
                    SUM(fpts) as total_fpts,
                    COUNT(*) as games_played
             FROM fantasy
             GROUP BY player_name
             ORDER BY avg_fpts DESC"""
  table = PlayerPointsTable(Fantasy.objects.raw(query))
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})


def team_average(request):
  from django.db import connection, transaction
  cursor = connection.cursor()
  data = []

  for team_id in xrange(1,9):
    query = """SELECT SUM(avg_fpts) as team_avg
               FROM (SELECT player_name, ROUND(AVG(fpts),2) as avg_fpts, MAX(period_id)
                     FROM fantasy
                     GROUP BY player_name
                     HAVING fteam = %i -- Change to team you want to find
                     ORDER BY period_id DESC
                     LIMIT 13);""" % team_id
    cursor.execute(query)
    team_avg = cursor.fetchone()[0]
    data.append({"team_id" : team_id, "team_avg" : team_avg})

  table = TeamAveragesTable(data)
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})
