from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from pathlib import Path
import shutil
import os

from ravnica import models, serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


class Command(BaseCommand):
    def handle(self, *args, **options):
        season: models.Season = models.Season.objects.get(pk=1)
        season.autoFill()
        print(season.standings)

        ser = serializers.SeasonSerializer(season)
        print(ser.data)