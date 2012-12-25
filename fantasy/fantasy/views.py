from django.http import HttpResponse
from fantasy.models import Fantasy
from django.shortcuts import render
import django_tables2 as tables

class FantasyTable(tables.Table):
  class Meta:
    model = Fantasy

def index(request):
  qs = Fantasy.objects.raw('SELECT player_name, round(avg(fpts),2) FROM fantasy GROUP BY player_name')
  table = FantasyTable(qs)
  tables.RequestConfig(request).configure(table)
  return render(request, "players.html", {"players": table})
