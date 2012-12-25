from django.http import HttpResponse
from fantasy.models import Fantasy

def index(request):
  names = []
  for player in Fantasy.objects.raw('SELECT DISTINCT player_name FROM fantasy'):
    names.append(player.player_name)
  return HttpResponse(names)