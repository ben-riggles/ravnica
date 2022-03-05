from django.db import models


class DeckLoadError(Exception):
    pass


class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    guild = models.ForeignKey('ravnica.Guild', on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    content = models.BinaryField()