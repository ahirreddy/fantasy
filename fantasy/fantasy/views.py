import json
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.db.models import Avg
from django.db.models import Max
from django_tables2 import RequestConfig
from fantasy.models import Fantasy
from fantasy.tables import *

def index(request):
  return HttpResponse("""
                      <a href="all_players">All Players</a>
                      <br />
                      <a href="multiple_team_players">Players who have been on multiple teams</a>
                      <br />
                      <a href="team_average">Roster Averages (Total)</a>
                      <br />
                      <a href="on_team_average">Roster Averages (While on Team)</a>
                      <br />
                      <a href="per_minute_fpts">Fantasy Points Per Minute</a>
                      <br />
                      <a href="per_position_rankings"><b>Per Position Rankings</b></a>
                      <br />
                      <a href="player_rankings">All Player Rankings/Positions</a>
                      """)

def all_players(request):
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

def multiple_team_players(request):
  query = """SELECT player_name, round(avg(fpts),2) as avg_fpts, fteam
             FROM fantasy
             GROUP BY player_name, fteam
             HAVING player_name IN (SELECT player_name
                                    FROM fantasy
                                    GROUP BY player_name
                                    HAVING COUNT(DISTINCT fteam) > 1)
            ORDER BY player_name, avg_fpts DESC;"""
  table = MultiplePlayerAveragesTable(Fantasy.objects.raw(query))
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})

def team_player_average_total(request):
  teams = []
  for team_id in xrange(1,9):
    query = """SELECT F.player_name as player_name, ROUND(AVG(F.fpts),2) as avg_fpts,
                      COUNT(*) as num_games
               FROM fantasy F, roster R
               WHERE F.player_name = R.player_name
                     AND R.fteam = %i
               GROUP BY F.player_name
               ORDER BY avg_fpts DESC""" % team_id
    qs = Fantasy.objects.raw(query)
    avg_total = 0
    for p in qs:
      avg_total += p.avg_fpts
    table = PlayerAveragesTable(qs)
    RequestConfig(request).configure(table)
    fpts = json.dumps([ [x.player_name, float(x.avg_fpts)] for x in qs])
    teams.append((team_id, avg_total, table, fpts))
  return render(request, "teams.html", {"teams" : teams})

def team_player_average_total_on_team(request):
  tables = []
  for team_id in xrange(1,9):
    query = """SELECT F.player_name as player_name, ROUND(AVG(F.fpts),2) as avg_fpts,
                      COUNT(*) as num_games
               FROM fantasy F, roster R
               WHERE F.player_name = R.player_name
                     AND R.fteam = %i
                     AND F.fteam = %i
               GROUP BY F.player_name""" % (team_id, team_id)
    qs = Fantasy.objects.raw(query)
    avg_total = sum([p.avg_fpts for p in qs])
    table = PlayerAveragesTable(qs)
    RequestConfig(request).configure(table)
    tables.append(("team%i" % team_id, avg_total, table))

  return render(request, "teams.html", {"teams" : tables})

def per_minute_fpts(request):
  query = """SELECT player_name, ROUND(CAST(CAST(total_fpts as float)/total_min as numeric),3) as per_minute_fpts
             FROM (SELECT player_name, SUM(fpts) as total_fpts, SUM(min) as total_min
                   FROM fantasy
                   GROUP BY player_name) as totals
             WHERE total_min > 48
             ORDER BY per_minute_fpts DESC;"""
  table = PerMinuteTable(Fantasy.objects.raw(query))
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})

def player_rankings(request):
  query = """ SELECT *, RANK() OVER (ORDER BY avg_fpts DESC) as rank
              FROM (SELECT F.player_name, ROUND(AVG(F.fpts),2) as avg_fpts, MAX(R.positions) as positions
                   FROM fantasy F, roster R
                   WHERE F.player_name = R.player_name
                   GROUP BY F.player_name
                   ORDER BY avg_fpts DESC) as subquery
         """
  table = RankingTable(Fantasy.objects.raw(query))
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})

def per_position_rankings(request):
  tables = []
  for position in ('PG', 'SG', 'SF', 'PF', 'C'):
    query = """ SELECT RANK() OVER (ORDER BY avg_fpts DESC) as rank, *
                FROM (
                      SELECT F.player_name, ROUND(AVG(F.fpts),2) as avg_fpts, MAX(R.positions) as positions
                      FROM fantasy F, roster R
                      WHERE F.player_name = R.player_name
                            AND substring(R.positions from '.$|..$|.,|..,') LIKE '%%{0}%%'
                      GROUP BY F.player_name
                      ORDER BY avg_fpts DESC
                     ) as subquery
                """.format(position)
    qs = Fantasy.objects.raw(query)
    total_fpts = sum([p.avg_fpts for p in qs])
    position_average = round(total_fpts/len(list(qs)),2)
    table = RankingTable(qs)
    RequestConfig(request).configure(table)
    tables.append((position, position_average, table))

  return render(request, "positions.html", {"category" : tables})

def individual_player(request):
  if request.method == 'GET' and 'player_name' in request.GET:
    player_name = request.GET['player_name']
    qs = Fantasy.objects.filter(player_name = player_name).order_by('-period_id')
    average = round(qs.aggregate(Avg('fpts'))['fpts__avg'],2)
    periods = json.dumps([x['period_id'] for x in qs.values('period_id')][::-1])
    fpts = json.dumps([float(x['fpts']) for x in qs.values('fpts')][::-1])

    return render(request, "player_charts.html", {"players" : qs, "average" : average, "periods" : periods, "fpts" : fpts})
  else:
    return HttpResponse("Must Provide Player Name")
