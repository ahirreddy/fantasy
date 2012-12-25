from django.http import HttpResponse
from fantasy.models import Fantasy
from django.shortcuts import render
from django_tables2 import RequestConfig
import django_tables2 as tables

class PlayerPointsTable(tables.Table):
  name = tables.Column(verbose_name="Player Name", accessor="player_name")
  avg_fpts = tables.Column(verbose_name="Avg Fpts", accessor="avg_fpts")
  total_fpts = tables.Column(verbose_name="Total Fpts", accessor="total_fpts")

def index(request):
  query = """SELECT player_name, round(avg(fpts),2) as avg_fpts, sum(fpts) as total_fpts
             FROM fantasy
             GROUP BY player_name
             ORDER BY avg_fpts DESC"""
  table = PlayerPointsTable(Fantasy.objects.raw(query))
  RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})
