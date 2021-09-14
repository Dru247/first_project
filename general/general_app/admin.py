from django.contrib import admin
from .models import Human, TelephoneNumber, Telegram, Terminals, SimCards, WialonUser, WialonObject, WialonObjectActive, UserWialonServer


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    empty_value_display = '-пусто-'


@admin.register(TelephoneNumber)
class TelephoneNumberAdmin(admin.ModelAdmin):
    list_display = ('human', 'number')
    search_fields = ('human',)
    empty_value_display = '-пусто-'


@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ('human', 'telegram_id',)
    search_fields = ('telegram_id',)
    empty_value_display = '-пусто-'


@admin.register(WialonUser)
class WialonUserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'password', 'human')
    search_fields = ('user_name',)
    empty_value_display = '-пусто-'


@admin.register(WialonObject)
class WialonObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'wialon_user', 'terminal')
    search_fields = ('name', 'terminal__imei')
    list_filter = ('wialon_user',)
    empty_value_display = '-пусто-'


@admin.register(WialonObjectActive)
class WialonObjectActiveAdmin(admin.ModelAdmin):
    list_display = ('wialon_object', 'active', 'last_modified')
    search_fields = ('wialon_object__name', )
    empty_value_display = '-пусто-'


@admin.register(Terminals)
class TerminalsAdmin(admin.ModelAdmin):
    list_display = ('imei', 'serial_number', 'model')
    search_fields = ('imei', 'serial_number')
    empty_value_display = '-пусто-'


@admin.register(SimCards)
class SimCardsAdmin(admin.ModelAdmin):
    list_display = ('number', 'icc', 'operator', 'terminal')
    search_fields = ('number', 'icc')
    empty_value_display = '-пусто-'


@admin.register(UserWialonServer)
class UserWialonServerAdmin(admin.ModelAdmin):
    list_display = ('user', 'server',)
    search_fields = ('user__user_name',)
    list_filter = ('server',)
    empty_value_display = '-пусто-'
