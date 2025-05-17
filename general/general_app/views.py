"""Файл для обработчиков запросов."""
import calendar
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, OuterRef
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics

from .models import (Human, HumanContact, HumanNames, HumanSimPresence,
                     HumanTerminalPresence, Installation, ModelTerminals,
                     PriceLogistics, PriceTrackers, Schedules, Services,
                     SimCards, Terminals, WialonObject, WialonServer,
                     WialonUser)
from .serializers import (HumanContactsSerializer, HumanNamesSerializer,
                          HumansSerializer, HumanSimPresenceSerializer,
                          HumanTerminalPresenceSerializer,
                          InstallationsSerializer, ModelTerminalsSerializer,
                          ObjectSerializer, PriceLogisticsSerializer,
                          PriceTrackersSerializer, ScheduleSerializer,
                          ServicesSerializer, SimSerializer,
                          SimCardMtsAllActiveSerializer, TerminalSerializer,
                          UsersSerializer)


class HumansAPIView(generics.ListAPIView):
    queryset = Human.objects.all()
    serializer_class = HumansSerializer


class HumanContactsAPIView(generics.ListAPIView):
    queryset = HumanContact.objects.all()
    serializer_class = HumanContactsSerializer


class HumanNamesAPIView(generics.ListAPIView):
    queryset = HumanNames.objects.all()
    serializer_class = HumanNamesSerializer


class HumanSimPresenceAPIView(generics.ListAPIView):
    queryset = HumanSimPresence.objects.all()
    serializer_class = HumanSimPresenceSerializer


class HumanTerminalPresenceAPIView(generics.ListAPIView):
    queryset = HumanTerminalPresence.objects.all()
    serializer_class = HumanTerminalPresenceSerializer


class InstallationsAPIView(generics.ListAPIView):
    queryset = Installation.objects.all()
    serializer_class = InstallationsSerializer


class ModelTerminalsAPIView(generics.ListAPIView):
    queryset = ModelTerminals.objects.all()
    serializer_class = ModelTerminalsSerializer


class ObjectAPIView(generics.ListAPIView):
    queryset = WialonObject.objects.all()
    serializer_class = ObjectSerializer


class ObjectsAPIUpdate(generics.UpdateAPIView):
    queryset = WialonObject.objects.all()
    serializer_class = ObjectSerializer


class PriceLogisticsAPIView(generics.ListAPIView):
    queryset = PriceLogistics.objects.all()
    serializer_class = PriceLogisticsSerializer


class PriceTrackersAPIView(generics.ListAPIView):
    queryset = PriceTrackers.objects.all()
    serializer_class = PriceTrackersSerializer


class ScheduleAPIView(generics.ListAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer


class ServicesAPIView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class SimAPIView(generics.ListAPIView):
    queryset = SimCards.objects.all()
    serializer_class = SimSerializer


class SimCardMtsAllActiveAPIView(generics.ListAPIView):
    """Возвращает все номера МТС в активных объектах."""

    queryset = SimCards.objects.values('number').filter(
        operator__name='МТС',
        number__isnull=False,
        terminal__terminal_glonass_objects__date_change_status__gt=(
            timezone.now()
        )
    ).values('number')
    serializer_class = SimCardMtsAllActiveSerializer


class TerminalAPIView(generics.ListAPIView):
    queryset = Terminals.objects.all()
    serializer_class = TerminalSerializer


class UsersAPIView(generics.ListAPIView):
    queryset = WialonUser.objects.all()
    serializer_class = UsersSerializer


@login_required
def index_view(request):
    """Отображение страницы проверок."""
    # sim_list = SimCards.objects.filter(
    #     terminal=None,
    #     humansimpresences__isnull=True
    # )
    # term_list = Terminals.objects.filter(
    #     wialonobjects__isnull=True,
    #     humanterminalpresence__isnull=True
    # )
    # # user_company_list = UserCompany.objects.all()
    # # user_list = (WialonUser.objects.filter(human=None)
    # #              .exclude(usercompany__in=user_company_list))
    # wia_obj_list = WialonObject.objects.filter(active__isnull=True)
    # sum_wia_obj = WialonObject.objects.filter(active=True).count()
    # sum_wia_obj_serv_active = Count(
    #     'userwialonservers__user__wialonobjects',
    #     filter=Q(userwialonservers__user__wialonobjects__active=True)
    # )
    # # sum_wia_obj_serv_active = Count(
    # #     'userwialonservers__user__wialonobjects__wialonobjectactive',
    # #     filter=Q(userwialonservers__user__wialonobjects__wialonobjectactive__active=True)
    # # )
    # wia_obj_serv_active = WialonServer.objects.annotate(
    #     active=sum_wia_obj_serv_active
    #     )
    # user_not_serv = WialonUser.objects.filter(userwialonserver__isnull=True)
    # context = {
    #     'sim_list': sim_list,
    #     'term_list': term_list,
    #     # 'user_list': user_list,
    #     'wia_obj_list': wia_obj_list,
    #     'wia_obj_serv_active': wia_obj_serv_active,
    #     'user_not_serv': user_not_serv,
    #     'sum_wia_obj': sum_wia_obj
    # }
    context = {}
    return render(request, 'general_app/index.html', context=context)


@login_required
def clients_view(request):
    """Отображение страницы оплаты."""
    # activ_obj_all = WialonObject.objects.filter(active=True).count()
    # not_activ_obj_all = WialonObject.objects.filter(active=False).count()
    # wialon_obj_all = Count('wialonuser__wialonobjects')
    # wialon_obj_active = Count(
    #     'wialonuser__wialonobjects',
    #     filter=Q(wialonuser__wialonobjects__active=True)
    # )
    # client_list = Human.objects.annotate(all=wialon_obj_all). \
    #     annotate(active=wialon_obj_active)
    months = ['', 'Январь', 'февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    first_day_next_month = ((datetime.datetime.today().replace(day=1)
                             + datetime.timedelta(days=32)).replace(day=1))
    human_list = Human.objects.raw(
        '''
        SELECT *, count(general_app_wialonobject.id) as active,
          sum(general_app_wialonobject.price) as cost
        FROM general_app_human
        JOIN general_app_wialonobject
          ON general_app_wialonobject.payer_id = general_app_human.id
        JOIN general_app_humannames
          ON general_app_humannames.id = general_app_human.name_id_id
        WHERE NOT general_app_wialonobject.date_change_status > %s
        AND general_app_wialonobject.active = 1
        GROUP BY general_app_human.id
        ORDER BY general_app_humannames.name, general_app_human.last_name
        ''',
        [first_day_next_month]
    )
    context = {
        'human_list': human_list,
        'month': months[first_day_next_month.month]
    }
    return render(request, 'general_app/clients.html', context=context)


@login_required
def get_without_payment(request):
    """Выводит список не оплативших клиентов за прошлый месяц."""
    date_now = datetime.date.today()
    past_month = date_now - relativedelta(months=1)
    past_month_last_day = calendar.monthrange(
        date_now.year,
        past_month.month
        )[1]
    date_target = past_month.strftime(f'%Y-%m-{past_month_last_day}')
    print(date_target)
    human_list = Human.objects.raw(
        '''
        SELECT *, count(general_app_wialonobject.id) as active,
          sum(general_app_wialonobject.price) as cost
        FROM general_app_human
        JOIN general_app_wialonobject
          ON general_app_wialonobject.payer_id = general_app_human.id
        JOIN general_app_humannames
          ON general_app_humannames.id = general_app_human.name_id_id
        WHERE general_app_wialonobject.date_change_status = %s
        AND general_app_wialonobject.active = 1
        GROUP BY general_app_human.id
        ORDER BY general_app_humannames.name, general_app_human.last_name
        ''',
        [date_target]
    )
    context = {
        'human_list': human_list
    }
    return render(request, 'general_app/without_payment.html', context=context)


@login_required
def server_view(request, server_id):
    """Считает кол-во объектов у клиентов по серверам."""
    # count_active_obj = Count(
    #     'usercompany__user_comp__wialonobjects',
    #     filter=Q(usercompany__user_comp__wialonobjects__active=True)
    # )
    # company_list = Company.objects.filter(
    #     usercompany__user_comp__in=active_users
    #     ).annotate(active=count_active_obj)

    # count_serv_all_active_obj = Count(
    #     'userwialonservers__user__wialonobjects',
    #     filter=Q(userwialonservers__user__wialonobjects__active=True)
    # )
    # serv_all_active_obj = (WialonServer.objects.filter(pk=server_id)
    #                        .annotate(active=count_serv_all_active_obj))

    serv_all_active_obj = WialonObject.objects.raw(
        """
        SELECT * FROM general_app_wialonobject
        JOIN general_app_wialonuser
        ON general_app_wialonuser.id = general_app_wialonobject.wialon_user_id
        WHERE general_app_wialonobject.date_change_status >= date('now')
        AND general_app_wialonuser.server_id = %s
        """,
        [server_id]
    )
    serv_all_active_obj = len(serv_all_active_obj)

    # server = get_object_or_404(WialonServer, pk=server_id)
    # active_users = WialonUser.objects.filter(
    #     userwialonserver__server=server,
    #     wialonobjects__active=True
    # )
    #
    # count_active_obj = Count(
    #     'wialonuser__wialonobjects',
    #     filter=Q(wialonuser__wialonobjects__active=True)
    # )
    # cost_month = Sum(
    #     'wialonuser__wialonobjects__price',
    #     filter=Q(wialonuser__wialonobjects__active=True)
    # )
    # human_list = Human.objects.filter(wialonuser__in=active_users) \
    #     .annotate(active=count_active_obj, cost=cost_month)

    human_list = Human.objects.raw(
        '''
        SELECT *, count(general_app_wialonobject.id) as active,
          sum(general_app_wialonobject.price) as cost
        FROM general_app_human
        JOIN general_app_wialonobject
          ON general_app_wialonobject.payer_id = general_app_human.id
        JOIN general_app_wialonuser
          ON general_app_wialonuser.id
            = general_app_wialonobject.wialon_user_id
        JOIN general_app_humannames
          ON general_app_humannames.id = general_app_human.name_id_id
        WHERE general_app_wialonuser.server_id = %s
        AND general_app_wialonobject.date_change_status >= date('now')
        GROUP BY general_app_human.id
        ORDER BY general_app_humannames.name, general_app_human.last_name
        ''',
        [server_id]
    )

    context = {
        'human_list': human_list,
        'serv_all_active_obj': serv_all_active_obj
    }
    return render(request, 'general_app/server.html', context=context)


@login_required
def delete_sim_view(request):
    """Выводит данные на страницу удаления СИМ-карт."""
    # date_now = datetime.datetime.now()
    # date_critical = date_now - relativedelta(months=3)
    # replace_date = date_now - relativedelta(months=5)

    # sim2m_list_delete = SimCards.objects.filter(
    #     terminal__wialonobjects__wialonobjectactive__last_modified__lte=date_critical,
    #     terminal__wialonobjects__wialonobjectactive__active=False,
    #     operator__name='СИМ2М'
    # ).annotate(
    #     data_deactivate=Max('terminal__wialonobjects__wialonobjectactive__last_modified')
    # ).order_by(
    #     'operator',
    #     'terminal__wialonobjects__wialonobjectactive__last_modified'
    # )

    sim2m_list_delete = WialonObject.objects.raw(
        '''
        SELECT general_app_simcards.id, general_app_simcards.number,
          general_app_wialonobject.date_change_status as date_target
        FROM general_app_simcards
        JOIN general_app_wialonobject
          ON general_app_wialonobject.terminal_id
            = general_app_simcards.terminal_id
        WHERE date_target < date('now', '-6 months')
        AND general_app_simcards.number
        AND general_app_simcards.operator_id = 3
        AND general_app_simcards.personal = 0
        AND general_app_wialonobject.active = 0
        '''
    )

    later_objects = WialonObject.objects.raw(
        '''
        SELECT general_app_wialonobject.id, general_app_wialonobject.name,
          general_app_wialonobject.date_change_status,
          general_app_human.last_name,
          general_app_humannames.name as payer_name,
          general_app_simcards.number,
          general_app_operatorssim.name as operator_name
        FROM general_app_wialonobject
        JOIN general_app_human
          ON general_app_wialonobject.payer_id = general_app_human.id
        JOIN general_app_wialonuser
          ON general_app_wialonuser.id
            = general_app_wialonobject.wialon_user_id
        JOIN general_app_humannames
          ON general_app_humannames.id = general_app_human.name_id_id
        JOIN general_app_simcards
          ON general_app_simcards.terminal_id
            = general_app_wialonobject.terminal_id
        JOIN general_app_operatorssim
          ON general_app_operatorssim.id = general_app_simcards.operator_id
        WHERE date_change_status < date('now', '-6 months')
        AND general_app_wialonobject.terminal_id
        AND general_app_simcards.terminal_id
        ORDER BY general_app_wialonobject.payer_id, date_change_status
        '''
    )

    # mts_last_replace = SimCards.objects.filter(
    #     terminal__wialonobjects__wialonobjectactive__last_modified__lte=replace_date,
    #     terminal__wialonobjects__wialonobjectactive__active=False,
    #     operator__name='МТС'
    # ).annotate(
    #     data_deactivate=Max('terminal__wialonobjects__wialonobjectactive__last_modified')
    # ).order_by('terminal__wialonobjects__wialonobjectactive__last_modified')

    mts_last_replace = SimCards.objects.raw(
        '''
        SELECT * FROM (
            SELECT general_app_simcards.id, general_app_simcards.number,
              general_app_wialonobject.date_change_status as date_target
            FROM general_app_simcards
            JOIN general_app_wialonobject
              ON general_app_wialonobject.terminal_id
                = general_app_simcards.terminal_id
            WHERE date_target < date('now', '-6 months')
            AND general_app_simcards.number
            AND general_app_simcards.operator_id = 2
            AND general_app_simcards.personal = 0
            AND general_app_wialonobject.active = 0
        )
        UNION
        SELECT * FROM (
            SELECT general_app_simcards.id, general_app_simcards.number,
              general_app_humansimpresence.time_create as date_target
            FROM general_app_simcards
            JOIN general_app_humansimpresence
              ON general_app_humansimpresence.simcard_id
                = general_app_simcards.id
            WHERE date_target < date('now', '-6 months')
            AND general_app_simcards.number
            AND general_app_simcards.operator_id = 2
            AND general_app_simcards.personal = 0
        )
        UNION
        SELECT * FROM (
            SELECT general_app_simcards.id, general_app_simcards.number,
              general_app_humanterminalpresence.time_create as date_target
            FROM general_app_simcards
            JOIN general_app_humanterminalpresence
              ON general_app_humanterminalpresence.terminal_id
                = general_app_simcards.terminal_id
            WHERE date_target < date('now', '-6 months')
            AND general_app_simcards.number
            AND general_app_simcards.operator_id = 2
            AND general_app_simcards.personal = 0
        )
        ORDER BY date_target
        LIMIT 5
        '''
    )

    context = {
        'sim2m_list_delete': sim2m_list_delete,
        'later_objects': later_objects,
        'mts_last_replace': mts_last_replace
    }
    return render(request, 'general_app/sim_delete.html', context=context)


@login_required
def maks_view(request):
    return render(request, 'general_app/maks_func.html')


@login_required
def info_view(request):
    return render(request, 'general_app/info_list.html')


@login_required
def reserve_view(request):
    symb_2011 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Start S-2011')
                 .filter(human__id='151').count())
    symb_2013 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Start S-2013')
                 .filter(human__id='151').count())
    symb_2421 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2421')
                 .filter(human__id='151').count())
    symb_2423 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2423')
                 .filter(human__id='151').count())
    symb_2425 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2425')
                 .filter(human__id='151').count())
    symb_2435 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2435')
                 .filter(human__id='151').count())
    symb_2437 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2437')
                 .filter(human__id='151').count())
    symb_333 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='ADM333')
                .filter(human__id='151').count())
    symb_007 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='ADM007 BLE в прикуриватель')
                .filter(human__id='151').count())
    symb_invis_duos = (HumanTerminalPresence.objects
                       .filter(terminal__model__model='Invis Duos')
                       .filter(human__id='151').count())
    symb_invis_duos_s = (HumanTerminalPresence.objects
                         .filter(terminal__model__model='Invis Duos S')
                         .filter(human__id='151').count())
    symb_invis_duos_3d_l = (HumanTerminalPresence.objects
                            .filter(terminal__model__model='Invis Duos 3D L')
                            .filter(human__id='151').count())
    symb_mts = (HumanSimPresence.objects
                .filter(simcard__operator__name='МТС')
                .filter(human__id='151').count())
    symb_mega = (HumanSimPresence.objects
                 .filter(simcard__operator__name='Мегафон')
                 .filter(human__id='151').count())
    symb_sim2m = (HumanSimPresence.objects
                  .filter(simcard__operator__name='СИМ2М')
                  .filter(human__id='151').count())

    malash_2011 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Start S-2011')
                   .filter(human__id='154').count())
    malash_2013 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Start S-2013')
                   .filter(human__id='154').count())
    malash_2421 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Smart S-2421')
                   .filter(human__id='154').count())
    malash_2423 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Smart S-2423')
                   .filter(human__id='154').count())
    malash_2425 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Smart S-2425')
                   .filter(human__id='154').count())
    malash_2435 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Smart S-2435')
                   .filter(human__id='154').count())
    malash_2437 = (HumanTerminalPresence.objects
                   .filter(terminal__model__model='Smart S-2437')
                   .filter(human__id='154').count())
    malash_333 = (HumanTerminalPresence.objects
                  .filter(terminal__model__model='ADM333')
                  .filter(human__id='154').count())
    malash_007 = (HumanTerminalPresence.objects
                  .filter(terminal__model__model='ADM007 BLE в прикуриватель')
                  .filter(human__id='154').count())
    malash_invis_duos = (HumanTerminalPresence.objects
                         .filter(terminal__model__model='Invis Duos')
                         .filter(human__id='154').count())
    malash_invis_duos_s = (HumanTerminalPresence.objects
                           .filter(terminal__model__model='Invis Duos S')
                           .filter(human__id='154').count())
    malash_invis_duos_3d_l = (HumanTerminalPresence.objects
                              .filter(terminal__model__model='Invis Duos 3D L')
                              .filter(human__id='154').count())
    malash_mts = (HumanSimPresence.objects
                  .filter(simcard__operator__name='МТС')
                  .filter(human__id='154').count())
    malash_mega = (HumanSimPresence.objects
                   .filter(simcard__operator__name='Мегафон')
                   .filter(human__id='154').count())
    malash_sim2m = (HumanSimPresence.objects
                    .filter(simcard__operator__name='СИМ2М')
                    .filter(human__id='154').count())

    leht_2011 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Start S-2011')
                 .filter(human__id='152').count())
    leht_2013 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Start S-2013')
                 .filter(human__id='152').count())
    leht_2421 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2421')
                 .filter(human__id='152').count())
    leht_2423 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2423')
                 .filter(human__id='152').count())
    leht_2425 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2425')
                 .filter(human__id='152').count())
    leht_2435 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2435')
                 .filter(human__id='152').count())
    leht_2437 = (HumanTerminalPresence.objects
                 .filter(terminal__model__model='Smart S-2437')
                 .filter(human__id='152').count())
    leht_333 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='ADM333')
                .filter(human__id='152').count())
    leht_007 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='ADM007 BLE в прикуриватель')
                .filter(human__id='152').count())
    leht_invis_duos = (HumanTerminalPresence.objects
                       .filter(terminal__model__model='Invis Duos')
                       .filter(human__id='152').count())
    leht_invis_duos_s = (HumanTerminalPresence.objects
                         .filter(terminal__model__model='Invis Duos S')
                         .filter(human__id='152').count())
    leht_invis_duos_3d_l = (HumanTerminalPresence.objects
                            .filter(terminal__model__model='Invis Duos 3D L')
                            .filter(human__id='152').count())
    leht_mts = (HumanSimPresence.objects
                .filter(simcard__operator__name='МТС')
                .filter(human__id='152').count())
    leht_mega = (HumanSimPresence.objects
                 .filter(simcard__operator__name='Мегафон')
                 .filter(human__id='152').count())
    leht_sim2m = (HumanSimPresence.objects
                  .filter(simcard__operator__name='СИМ2М')
                  .filter(human__id='152').count())

    yar_2420 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='Smart S-2420')
                .filter(human__id='501').count())
    yar_2421 = (HumanTerminalPresence.objects
                .filter(terminal__model__model='Smart S-2421')
                .filter(human__id='501').count())

    context = {
        'symb_2011': symb_2011,
        'symb_2013': symb_2013,
        'symb_2421': symb_2421,
        'symb_2423': symb_2423,
        'symb_2425': symb_2425,
        'symb_2435': symb_2435,
        'symb_2437': symb_2437,
        'symb_333': symb_333,
        'symb_007': symb_007,
        'symb_invis_duos': symb_invis_duos,
        'symb_invis_duos_s': symb_invis_duos_s,
        'symb_invis_duos_3d_l': symb_invis_duos_3d_l,
        'symb_mts': symb_mts,
        'symb_mega': symb_mega,
        'symb_sim2m': symb_sim2m,
        'malash_2011': malash_2011,
        'malash_2013': malash_2013,
        'malash_2421': malash_2421,
        'malash_2423': malash_2423,
        'malash_2425': malash_2425,
        'malash_2435': malash_2435,
        'malash_2437': malash_2437,
        'malash_333': malash_333,
        'malash_007': malash_007,
        'malash_invis_duos': malash_invis_duos,
        'malash_invis_duos_s': malash_invis_duos_s,
        'malash_invis_duos_3d_l': malash_invis_duos_3d_l,
        'malash_mts': malash_mts,
        'malash_mega': malash_mega,
        'malash_sim2m': malash_sim2m,
        'leht_2011': leht_2011,
        'leht_2013': leht_2013,
        'leht_2421': leht_2421,
        'leht_2423': leht_2423,
        'leht_2425': leht_2425,
        'leht_2435': leht_2435,
        'leht_2437': leht_2437,
        'leht_333': leht_333,
        'leht_007': leht_007,
        'leht_invis_duos': leht_invis_duos,
        'leht_invis_duos_s': leht_invis_duos_s,
        'leht_invis_duos_3d_l': leht_invis_duos_3d_l,
        'leht_mts': leht_mts,
        'leht_mega': leht_mega,
        'leht_sim2m': leht_sim2m,
        'yar_2420': yar_2420,
        'yar_2421': yar_2421
    }

    return render(request, 'general_app/reserve.html', context=context)
