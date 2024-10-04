from rest_framework import serializers
from .models import SimCards, Terminals, WialonObject


class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimCards
        fields = ('id', 'operator', 'number', 'icc', 'terminal')


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminals
        fields = ('id', 'imei')


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonObject
        fields = ('terminal', 'payer', 'active', 'date_change_status')
