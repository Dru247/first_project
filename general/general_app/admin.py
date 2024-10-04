from django.contrib import admin
from django.db.models import Count, Q

from .models import (HumanNames, Human, HumanSimPresence, HumanTerminalPresence, SimCards,
                     Telegram, TelephoneNumber, Terminals, UserWialonServer,
                     WialonObject, WialonObjectActive, WialonUser, Company,
                     UserCompany, HumanCompany, Contact, HumanContact,
                     BrandTerminals, ModelTerminals, BrandCar, ModelCar,
                     Installation, InstallationComment)


@admin.register(HumanNames)
class HumanNamesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-'


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_id', 'last_name', 'description')
    search_fields = ('name_id', 'last_name')
    autocomplete_fields = ('name_id',)
    empty_value_display = '-'


@admin.register(HumanContact)
class HumanContactAdmin(admin.ModelAdmin):
    list_display = ('human', 'contact', 'contact_rec')
    search_fields = ('human__first_name', 'human__last_name', 'contact_rec',)
    autocomplete_fields = ('human',)
    empty_value_display = '-'


@admin.register(WialonUser)
class WialonUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_name',
        'human',
        'server',
        'active_objs',
        'payment',
        'comment'
    )
    autocomplete_fields = ('human',)
    search_fields = ('user_name', 'human__first_name', 'human__last_name')
    list_filter = ('payment',)
    empty_value_display = '-'

    @admin.display(description="Сервер")
    def server(self, obj):
        return UserWialonServer.objects.get(user=obj).server

    @admin.display(
        description="Кол-во"
    )
    def active_objs(self, obj):
        count_objs = WialonObject.objects.filter(
            wialon_user=obj,
            wialonobjectactive__active=True,
            ).count()
        return count_objs


@admin.register(WialonObject)
class WialonObjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'wialon_user',
        'terminal',
        # 'active',
        # 'last_change',
        # 'sim',
        'price',
        'payer',
        'active',
        'date_change_status',
        'comment'
    )
    search_fields = ('name', 'wialon_user__user_name', 'terminal__imei')
    autocomplete_fields = ('terminal', 'wialon_user', 'payer')
    list_filter = ('payer',)
    empty_value_display = '-'

    # @admin.display(
    #     description="Посл. изменения",
    #     ordering='wialonobjectactive__last_modified'
    # )
    # def last_change(self, obj):
    #     return WialonObjectActive.objects.get(wialon_object=obj).last_modified
    #
    # @admin.display(description="Статус")
    # def active(self, obj):
    #     return WialonObjectActive.objects.get(wialon_object=obj).active

#    @admin.display(description="СИМ-карты")
#    def sim(self, obj):
#        sim_list = [sim for sim in SimCards.objects.filter(terminal=obj.terminal)]
#        return sim_list


# @admin.register(WialonObjectActive)
# class WialonObjectActiveAdmin(admin.ModelAdmin):
#     list_display = ('wialon_object', 'active',)
#     search_fields = ('wialon_object__name', )
#     autocomplete_fields = ('wialon_object',)
#     empty_value_display = '-пусто-'


@admin.register(BrandTerminals)
class BrandTerminalsAdmin(admin.ModelAdmin):
    list_display = ('brand',)
    empty_value_display = '-'


@admin.register(ModelTerminals)
class ModelTerminalsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model',)
    empty_value_display = '-'


@admin.register(Terminals)
class TerminalsAdmin(admin.ModelAdmin):
    list_display = ('imei', 'serial_number', 'model', 'time_create')
    search_fields = ('imei', 'serial_number')
    empty_value_display = '-'


@admin.register(SimCards)
class SimCardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'icc', 'operator', 'number', 'terminal', 'time_create')
    search_fields = ('number', 'icc', 'terminal__imei')
    autocomplete_fields = ('terminal',)
    list_filter = ('operator',)


@admin.register(UserWialonServer)
class UserWialonServerAdmin(admin.ModelAdmin):
    list_display = ('user', 'server',)
    search_fields = ('user__user_name',)
    autocomplete_fields = ('user',)
    list_filter = ('server',)
    empty_value_display = '-'


@admin.register(HumanTerminalPresence)
class HumanTerminalPresenceAdmin(admin.ModelAdmin):
    list_display = (
        'human',
        'terminal',
        'terminal_model',
        'terminal_serial_number',
        'time_create'
    )
    search_fields = (
        'terminal__imei',
        'terminal__serial_number',
        'human__last_name',
        'human__first_name'
    )
    autocomplete_fields = ('human', 'terminal')
    list_filter = ('terminal__model',)
    empty_value_display = '-'

    @admin.display()
    def terminal_model(self, obj):
        return obj.terminal.model

    @admin.display()
    def terminal_serial_number(self, obj):
        return obj.terminal.serial_number


@admin.register(HumanSimPresence)
class HumanSimPresenceAdmin(admin.ModelAdmin):
    list_display = (
        'human',
        'simcard',
        'simcard_icc',
        'simcard_operator',
        'time_create'
    )
    search_fields = (
        'simcard__number',
        'simcard__icc',
        'human__first_name',
        'human__last_name'
    )
    autocomplete_fields = ('human', 'simcard')
    list_filter = ('simcard__operator',)
    empty_value_display = '-'

    @admin.display()
    def simcard_icc(self, obj):
        return obj.simcard.icc

    @admin.display()
    def simcard_operator(self, obj):
        return obj.simcard.operator


# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#    search_fields = ('name',)
#    empty_value_display = '-пусто-'
#
#
# @admin.register(HumanCompany)
# class HumanCompanyAdmin(admin.ModelAdmin):
#    list_display = ('company_hum', 'human_comp')
#    search_fields = (
#        'human_comp__first_name',
#        'human_comp__first_name',
#        'company_hum'
#    )
#    autocomplete_fields = ('human_comp',)
#    empty_value_display = '-пусто-'
#
#
# @admin.register(UserCompany)
# class HumanCompanyAdmin(admin.ModelAdmin):
#    list_display = ('company_us', 'user_comp')
#    search_fields = ('user_comp__user_name', 'company_us_name',)
#    autocomplete_fields = ('company_us', 'user_comp')
#    empty_value_display = '-пусто-'


@admin.register(BrandCar)
class BrandCarAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-'


@admin.register(ModelCar)
class ModelCarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')
    search_fields = ('brand', 'name')
    empty_value_display = '-'


@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'location',
        'model',
        'vin',
        'state_number',
        'terminal',
        'human_worker',
        'user',
        'juristic_person',
        'payment',
        'comment'
    )
    autocomplete_fields = (
        'model',
        'terminal',
        'human_worker',
        'user'
    )
    search_fields = (
        'state_number',
        'vin',
        'terminal__imei',
        'model__brand__name',
        'model__name',
        'user__user_name'
    )
    empty_value_display = '-'

    # @admin.display()
    # def comment(self, obj):
    #     return InstallationComment.objects.get(installation=obj).text


# @admin.register(InstallationComment)
# class InstallationCommentAdmin(admin.ModelAdmin):
#     list_display = ('installation', 'text')
#     autocomplete_fields = ('installation',)
#     search_fields = ('installation__terminal__imei', 'text')
#     empty_value_display = 'пусто'
