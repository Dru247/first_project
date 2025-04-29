from rest_framework import serializers

from .models import (Human, HumanContact, HumanNames, HumanSimPresence,
                     HumanTerminalPresence, Installation, ModelTerminals,
                     PriceLogistics, PriceTrackers, Schedules, Services,
                     SimCards, Terminals, WialonObject, WialonUser)


class HumansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = '__all__'


class HumanContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanContact
        fields = '__all__'


class HumanNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanNames
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


class ModelTerminalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTerminals
        fields = '__all__'


class PriceLogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceLogistics
        fields = '__all__'


class PriceTrackersSerializer(serializers.ModelSerializer):
    tracker_model = serializers.StringRelatedField()

    class Meta:
        model = PriceTrackers
        fields = ('tracker_model', 'cost')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('service', 'cost')


class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimCards
        fields = '__all__'


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminals
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonObject
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WialonUser
        fields = '__all__'
