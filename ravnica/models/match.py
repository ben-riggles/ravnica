from django.db import models


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    round = models.ForeignKey('ravnica.Round', on_delete=models.CASCADE)
    away = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='deck_away')
    home = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='deck_home')
    winner = models.ForeignKey('ravnica.Deck', default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='deck_winner')