from django.http import HttpResponse
from fantasy.models import Fantasy
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.db.models.query import QuerySet
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

  players = []
  for p in Fantasy.objects.raw(query):
    players.append({"player_name" : p.player_name,
                    "avg_fpts" : p.avg_fpts,
                    "total_fpts" : p.total_fpts,
                    "games_played" : p.games_played})

  table = PlayerPointsTable(players)
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

class PlayerAveragesTable(tables.Table):
  player_name = tables.Column(verbose_name="Player Name")
  avg_fpts = tables.Column(verbose_name="FPTS Avg")

  class Meta:
    attrs = {"class": "paleblue"}

def team_player_average_total(request):
  query = """SELECT F.player_name as player_name, ROUND(AVG(F.fpts),2) as avg_fpts
             FROM fantasy F, roster R
             WHERE F.player_name = R.player_name
                   AND R.fteam = %i
             GROUP BY F.player_name""" % 2

  data = []
  for p in Fantasy.objects.raw(query):
    data.append({'player_name' : p.player_name,
                 'avg_fpts' : p.avg_fpts})

  table = PlayerAveragesTable(data)
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})

def team_player_average_total_on_team(request):
  tables = []
  for team_id in xrange(1,9):
    query = """SELECT F.player_name as player_name, ROUND(AVG(F.fpts),2) as avg_fpts
               FROM fantasy F, roster R
               WHERE F.player_name = R.player_name
                     AND R.fteam = %i
                     AND F.fteam = %i
               GROUP BY F.player_name""" % (team_id, team_id)

    data = []
    for p in Fantasy.objects.raw(query):
      data.append({'player_name' : p.player_name,
                   'avg_fpts' : p.avg_fpts})

    table = PlayerAveragesTable(data)
    RequestConfig(request).configure(table)
    tables.append(table)

  return render(request, "teams.html", {"team1": tables[0], "team2" : tables[1]})