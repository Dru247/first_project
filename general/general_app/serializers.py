from rest_framework import serializers
from .models import *


class HumanContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanContact
        fields = '__all__'


class HumanSimPresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanSimPresence
        fields = '__all__'


class HumanTerminalPresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanTerminalPresence
        fields = '__all__'


class InstallationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonObject
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'


class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimCards
        fields = '__all__'


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminals
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonUser
        fields = '__all__'
