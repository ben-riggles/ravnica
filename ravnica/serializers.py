import logging
from rest_framework import serializers

from ravnica import models, enums


class RecordSerializer(serializers.Serializer):
    wins = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    win_pct = serializers.FloatField(read_only=True)

    def to_internal_value(self, data):
        try:
            return models.Record(
                wins=data['wins'],
                losses=data['losses']
            )
        except KeyError:
            logging.error('Error deserializing Record: ' + data)
        return None


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guild
        fields = ('id', 'name', 'full_name', 'short_name')


class DeckSerializer(serializers.ModelSerializer):
    guild = GuildSerializer(read_only=True)

    class Meta:
        model = models.Deck
        fields = ('id', 'guild', 'current', 'name')


class MatchSerializer(serializers.ModelSerializer):
    season = serializers.PrimaryKeyRelatedField(read_only=True)
    away = DeckSerializer(read_only=True)
    home = DeckSerializer(read_only=True)
    winner = DeckSerializer()
    
    class Meta:
        model = models.Match
        fields = ('id', 'season', 'round', 'away', 'home', 'winner')


class StandingsSerializer(serializers.Serializer):
    season = serializers.PrimaryKeyRelatedField(read_only=True)
    guild = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.ChoiceField(choices=enums.RecordType, read_only=True)
    data = serializers.SerializerMethodField()

    def get_data(self, obj: models.Standings):
        return [{
            'guild': GuildSerializer(guild).data,
            'record': RecordSerializer(record).data
        } for (guild, record) in obj]


class SeasonSerializer(serializers.ModelSerializer):
    previous = serializers.PrimaryKeyRelatedField(read_only=True)
    standings = StandingsSerializer(read_only=True)
    
    class Meta:
        model = models.Season
        fields = ('id', 'number', 'name', 'previous', 'standings')
        
        

        
        




