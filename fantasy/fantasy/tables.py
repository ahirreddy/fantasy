import django_tables2 as tables

class PlayerPointsTable(tables.Table):
  player_name = tables.TemplateColumn('<a href="/individual_player?player_name={{record.player_name}}">{{record.player_name}}</a>', verbose_name="Player Name")
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

class PlayerAveragesTable(tables.Table):
  player_name = tables.TemplateColumn('<a href="/individual_player?player_name={{record.player_name}}">{{record.player_name}}</a>', verbose_name="Player Name")
  avg_fpts = tables.Column(verbose_name="FPTS Avg")
  num_games = tables.Column(verbose_name="# Games")
  class Meta:
    attrs = {"class": "paleblue"}

class MultiplePlayerAveragesTable(PlayerAveragesTable):
  fteam = tables.Column(verbose_name="Fteam")
  class Meta:
    attrs = {"class": "paleblue"}

class PerMinuteTable(tables.Table):
  player_name = tables.TemplateColumn('<a href="/individual_player?player_name={{record.player_name}}">{{record.player_name}}</a>', verbose_name="Player Name")
  per_minute_fpts = tables.Column(verbose_name="Avg Fpts")
  class Meta:
    attrs = {"class": "paleblue"}

class RankingTable(tables.Table):
  rank = tables.Column(verbose_name="Rank")
  player_name = tables.TemplateColumn('<a href="/individual_player?player_name={{record.player_name}}">{{record.player_name}}</a>', verbose_name="Player Name")
  avg_fpts = tables.Column(verbose_name="Avg Fpts")
  positions = tables.Column(verbose_name="Positions")
  class Meta:
    attrs = {"class": "paleblue"}

class IndividualPlayerTable(tables.Table):
  class Meta:
    attrs = {"class": "paleblue"}