from django.contrib import admin

from .models import (Human, HumanSimPresence, HumanTerminalPresence, SimCards,
                     Telegram, TelephoneNumber, Terminals, UserWialonServer,
                     WialonObject, WialonObjectActive, WialonUser, Company,
                     UserCompany, HumanCompany, Contact, HumanContact)


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    empty_value_display = '-пусто-'


@admin.register(HumanContact)
class HumanContactAdmin(admin.ModelAdmin):
    list_display = ('human', 'contact', 'contact_rec')
    search_fields = ('human__first_name', 'human__last_name', 'contact_rec',)
    autocomplete_fields = ('human',)
    empty_value_display = '-пусто-'


@admin.register(WialonUser)
class WialonUserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'password', 'human')
    autocomplete_fields = ('human',)
    search_fields = ('user_name', 'human__first_name', 'human__last_name')
    empty_value_display = '-пусто-'


@admin.register(WialonObject)
class WialonObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'wialon_user', 'terminal', 'active')
    search_fields = ('name', 'wialon_user__user_name', 'terminal__imei')
    autocomplete_fields = ('terminal', 'wialon_user')
    list_filter = ('wialon_user',)
    empty_value_display = '-пусто-'

    @admin.display()
    def active(self, obj):
        return WialonObjectActive.objects.get(wialon_object=obj).active


@admin.register(WialonObjectActive)
class WialonObjectActiveAdmin(admin.ModelAdmin):
    list_display = ('wialon_object', 'active',)
    search_fields = ('wialon_object__name', )
    autocomplete_fields = ('wialon_object',)
    empty_value_display = '-пусто-'


@admin.register(Terminals)
class TerminalsAdmin(admin.ModelAdmin):
    list_display = ('imei', 'serial_number', 'model')
    search_fields = ('imei', 'serial_number')
    empty_value_display = '-пусто-'


@admin.register(SimCards)
class SimCardsAdmin(admin.ModelAdmin):
    list_display = ('number', 'icc', 'operator', 'terminal')
    search_fields = ('number', 'icc', 'terminal__imei')
    autocomplete_fields = ('terminal',)
    empty_value_display = '-пусто-'


@admin.register(UserWialonServer)
class UserWialonServerAdmin(admin.ModelAdmin):
    list_display = ('user', 'server',)
    search_fields = ('user__user_name',)
    autocomplete_fields = ('user',)
    list_filter = ('server',)
    empty_value_display = '-пусто-'


@admin.register(HumanTerminalPresence)
class HumanTerminalPresenceAdmin(admin.ModelAdmin):
    list_display = (
        'human',
        'terminal',
        'terminal_model',
        'terminal_serial_number'
    )
    search_fields = ('terminal__imei', 'terminal__serial_number')
    autocomplete_fields = ('human', 'terminal')
    list_filter = ('human',)
    empty_value_display = '-пусто-'

    @admin.display()
    def terminal_model(self, obj):
        return obj.terminal.model

    @admin.display()
    def terminal_serial_number(self, obj):
        return obj.terminal.serial_number


@admin.register(HumanSimPresence)
class HumanSimPresenceAdmin(admin.ModelAdmin):
    list_display = ('human', 'simcard', 'simcard_icc')
    search_fields = ('simcard__number', 'simcard__icc')
    autocomplete_fields = ('human', 'simcard')
    list_filter = ('human',)
    empty_value_display = '-пусто-'

    @admin.display()
    def simcard_icc(self, obj):
        return obj.simcard.icc


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(HumanCompany)
class HumanCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_hum', 'human_comp')
    search_fields = ('human_comp__first_name', 'human_comp__first_name', 'company_hum')
    autocomplete_fields = ('human_comp',)
    empty_value_display = '-пусто-'


@admin.register(UserCompany)
class HumanCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_us', 'user_comp')
    search_fields = ('user_comp__user_name', 'company_us_name',)
    autocomplete_fields = ('company_us', 'user_comp')
    empty_value_display = '-пусто-'
