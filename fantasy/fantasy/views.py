from django.http import HttpResponse
from fantasy.models import Fantasy
from django.shortcuts import render

def index(request):
  qs = Fantasy.objects.raw('SELECT player_name, round(avg(fpts),2) as avg_fpts FROM fantasy GROUP BY player_name ORDER BY avg_fpts DESC')
  return render(request, "players.html", {"players": qs})
