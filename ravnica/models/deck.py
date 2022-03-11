from django.db import models

from core.models import Record


class DeckLoadError(Exception):
    pass


class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    guild = models.ForeignKey('ravnica.Guild', on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    content = models.BinaryField()
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        name = self.name if self.name else 'N/A'
        return f'{name} ({self.guild.name})'

    def __repr__(self):
        name = self.name if self.name else 'N/A'
        return f'Deck({self.guild.name} "{name}")'

    def record(self, season:'Season' = None, versus:'Guild' = None) -> Record:
        match_set = self.away_set.all() | self.home_set.all()
        if season is not None:
            match_set = match_set.filter(season=season)
        if versus is not None:
            match_set = match_set.filter(models.Q(away__guild = versus) | models.Q(home__guild = versus))
            
        win_count = len(match_set.filter(winner=self))
        return Record(wins=win_count, losses=len(match_set) - win_count)