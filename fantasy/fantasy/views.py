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
  return HttpResponse("""
                      <a href="all_players">All Players</a>
                      <br />
                      <a href="multiple_team_players">Players who have been on multiple teams</a>
                      <br />
                      <a href="team_average">Roster Averages (Total)</a>
                      <br />
                      <a href="on_team_average">Roster Averages (While on Team)</a>
                      """)

def all_players(request):
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

def multiple_team_players(request):
  from django.db import connection, transaction
  cursor = connection.cursor()
  data = []

  query = """SELECT player_name, round(avg(fpts),2) as avg_fpts, fteam
             FROM fantasy
             GROUP BY player_name, fteam
             HAVING player_name IN (SELECT player_name
                                    FROM fantasy
                                    GROUP BY player_name
                                    HAVING COUNT(DISTINCT fteam) > 1)
            ORDER BY player_name, avg_fpts DESC;"""

  for p in Fantasy.objects.raw(query):
    data.append({'player_name' : p.player_name,
                 'avg_fpts' : p.avg_fpts,
                 'fteam' : p.fteam})

  table = MultiplePlayerAveragesTable(data)
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})

class PlayerAveragesTable(tables.Table):
  player_name = tables.Column(verbose_name="Player Name")
  avg_fpts = tables.Column(verbose_name="FPTS Avg")

  class Meta:
    attrs = {"class": "paleblue"}

class MultiplePlayerAveragesTable(PlayerAveragesTable):
  fteam = tables.Column(verbose_name="Fteam")

  class Meta:
    attrs = {"class": "paleblue"}

def team_player_average_total(request):
  tables = []
  for team_id in xrange(1,9):
    query = """SELECT F.player_name as player_name, ROUND(AVG(F.fpts),2) as avg_fpts
               FROM fantasy F, roster R
               WHERE F.player_name = R.player_name
                     AND R.fteam = %i
               GROUP BY F.player_name""" % team_id

    data = []
    avg_total = 0
    for p in Fantasy.objects.raw(query):
      data.append({'player_name' : p.player_name,
                   'avg_fpts' : p.avg_fpts})
      avg_total += p.avg_fpts

    table = PlayerAveragesTable(data)
    RequestConfig(request).configure(table)
    tables.append(("team%i" % team_id, avg_total, table))
  return render(request, "teams.html", {"teams" : tables})

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
    avg_total = 0
    for p in Fantasy.objects.raw(query):
      data.append({'player_name' : p.player_name,
                   'avg_fpts' : p.avg_fpts})
      avg_total += p.avg_fpts

    table = PlayerAveragesTable(data)
    RequestConfig(request).configure(table)
    tables.append(("team%i" % team_id, avg_total, table))

  return render(request, "teams.html", {"teams" : tables})
