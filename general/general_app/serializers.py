from rest_framework import serializers
from .models import SimCards, Terminals


class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimCards
        fields = ('id', 'operator', 'number', 'icc', 'terminal')


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminals
        fields = ('id', 'imei')
