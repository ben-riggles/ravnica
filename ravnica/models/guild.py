from django.db import models

from ravnica.models import Deck


class Guild(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=50)

    @property
    def current_deck(self) -> Deck:
        return self.deck_set.get(current=True)