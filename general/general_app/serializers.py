from rest_framework import serializers
from .models import *


class HumanContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanContact
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonObject
        fields = '__all__'


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
