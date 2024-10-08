from rest_framework import serializers
from .models import SimCards, Terminals, WialonObject, WialonUser


class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimCards
        fields = ('id', 'operator', 'number', 'icc', 'terminal')


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminals
        fields = ('id', 'imei')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonUser
        fields = ('id', 'server', 'user_name')


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonObject
        fields = ('name', 'wialon_user', 'terminal', 'payer', 'active', 'date_change_status')
