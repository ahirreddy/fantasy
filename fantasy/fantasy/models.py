# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Fantasy(models.Model):
    player_name = models.TextField(blank=True, primary_key=True)
    fteam = models.IntegerField(null=True, blank=True)
    fgm = models.IntegerField(null=True, blank=True)
    fga = models.IntegerField(null=True, blank=True)
    ftm = models.IntegerField(null=True, blank=True)
    fta = models.IntegerField(null=True, blank=True)
    reb = models.IntegerField(null=True, blank=True)
    ast = models.IntegerField(null=True, blank=True)
    stl = models.IntegerField(null=True, blank=True)
    blk = models.IntegerField(null=True, blank=True)
    tover = models.IntegerField(null=True, blank=True)
    pts = models.IntegerField(null=True, blank=True)
    fpts = models.IntegerField(null=True, blank=True)
    opp = models.TextField(blank=True)
    slot = models.TextField(blank=True)
    period_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'fantasy'

