import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.shortcuts import get_object_or_404, render
from django.db.models import Max

from .models import (Human, SimCards, Terminals, WialonObject, HumanTerminalPresence,
                     WialonObjectActive, WialonUser, WialonServer, Company, UserCompany,
                     HumanSimPresence)


@login_required
def index_view(request):
    sim_list = SimCards.objects.filter(
        terminal=None,
        humansimpresences__isnull=True
    )
    term_list = Terminals.objects.filter(
        wialonobjects__isnull=True,
        humanterminalpresence__isnull=True
    )
    user_company_list = UserCompany.objects.all()
    user_list = WialonUser.objects.filter(human=None).exclude(usercompany__in=user_company_list)
    wia_obj_list = WialonObject.objects.filter(wialonobjectactive__isnull=True)
    sum_wia_obj = WialonObject.objects.filter(wialonobjectactive__active=True).count()
    sum_wia_obj_serv_active = Count(
        'userwialonservers__user__wialonobjects__wialonobjectactive',
        filter=Q(userwialonservers__user__wialonobjects__wialonobjectactive__active=True)
    )
    wia_obj_serv_active = WialonServer.objects.annotate(active=sum_wia_obj_serv_active)
    user_not_serv = WialonUser.objects.filter(userwialonserver__isnull=True)
    context = {
        'sim_list': sim_list,
        'term_list': term_list,
        'user_list': user_list,
        'wia_obj_list': wia_obj_list,
        'wia_obj_serv_active': wia_obj_serv_active,
        'user_not_serv': user_not_serv,
        'sum_wia_obj': sum_wia_obj
    }
    return render(request, 'general_app/index.html', context=context)


@login_required
def clients_view(request):
    activ_obj_all = len(WialonObjectActive.objects.filter(active=True))
    not_activ_obj_all = len(WialonObjectActive.objects.filter(active=False))
    wialon_obj_all = Count('wialonuser__wialonobjects')
    wialon_obj_active = Count(
        'wialonuser__wialonobjects__wialonobjectactive',
        filter=Q(wialonuser__wialonobjects__wialonobjectactive__active=True)
    )
    client_list = Human.objects.annotate(all=wialon_obj_all). \
        annotate(active=wialon_obj_active)
    context = {
        'client_list': client_list,
        'activ_obj_all': activ_obj_all,
        'not_activ_obj_all': not_activ_obj_all,
    }
    return render(request, 'general_app/clients.html', context=context)


@login_required
def server_view(request, server_id):
    # count all active objects on the server
    count_serv_all_active_obj = Count(
        'userwialonservers__user__wialonobjects__wialonobjectactive',
        filter=Q(userwialonservers__user__wialonobjects__wialonobjectactive__active=True)
    )
    serv_all_active_obj = WialonServer.objects.filter(pk=server_id).annotate(active=count_serv_all_active_obj)

    serv_now = get_object_or_404(WialonServer, pk=server_id)
    active_users = WialonUser.objects.filter(
        userwialonserver__server=serv_now,
        wialonobjects__wialonobjectactive__active=True
    )

    # view list companies width count active objects
    count_active_obj = Count(
        'usercompany__user_comp__wialonobjects',
        filter=Q(usercompany__user_comp__wialonobjects__wialonobjectactive__active=True)
    )
    company_list = Company.objects.filter(usercompany__user_comp__in=active_users).annotate(active=count_active_obj)

    # view list clients width count active objects
    count_active_obj = Count(
        'wialonuser__wialonobjects',
        filter=Q(wialonuser__wialonobjects__wialonobjectactive__active=True)
    )
    cost_month = Sum(
        'wialonuser__wialonobjects__price',
        filter=Q(wialonuser__wialonobjects__wialonobjectactive__active=True)
    )
    human_list = Human.objects.filter(wialonuser__in=active_users).annotate(active=count_active_obj, cost=cost_month)

    context = {
        'human_list': human_list,
        'company_list': company_list,
        'serv_all_active_obj': serv_all_active_obj
    }
    return render(request, 'general_app/server.html', context=context)


@login_required
def delete_sim_view(request):
    date_1 = datetime.datetime.now()
    year_now = date_1.year
    month_now = date_1.month
    if month_now < 6:
        month_now = date_1.month + 12
    replace_date = datetime.datetime.today() - relativedelta(months=6)
    sim_list_delete = SimCards.objects.filter(
        terminal__wialonobjects__wialonobjectactive__last_modified__month__lte=month_now,
        terminal__wialonobjects__wialonobjectactive__active=False
    ).exclude(
        terminal__wialonobjects__wialonobjectactive__last_modified__year=year_now
    ).annotate(
        data_deactivate=Max('terminal__wialonobjects__wialonobjectactive__last_modified')
    ).order_by('operator')
    sim_list_replace = SimCards.objects.filter(
        terminal__wialonobjects__wialonobjectactive__last_modified__lte=replace_date,
        terminal__wialonobjects__wialonobjectactive__active=False,
        operator__name='МТС'
    ).annotate(
        data_deactivate=Max('terminal__wialonobjects__wialonobjectactive__last_modified')
    ).order_by('terminal__wialonobjects__wialonobjectactive__last_modified')

    context = {
        'sim_list': sim_list_delete,
        'sim_list_replace': sim_list_replace
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
    symb_2011 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2011').filter(human__id='151').count()
    symb_2013 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2013').filter(human__id='151').count()
    symb_2421 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2421').filter(human__id='151').count()
    symb_2423 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2423').filter(human__id='151').count()
    symb_2425 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2425').filter(human__id='151').count()
    symb_2435 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2435').filter(human__id='151').count()
    symb_2437 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2437').filter(human__id='151').count()
    symb_333 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM333').filter(human__id='151').count()
    symb_007 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM007 BLE в прикуриватель').filter(human__id='151').count()
    symb_invis_duos = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos').filter(human__id='151').count()
    symb_invis_duos_s = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos S').filter(human__id='151').count()
    symb_invis_duos_3d_l = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos 3D L').filter(human__id='151').count()
    symb_mts = HumanSimPresence.objects.filter(simcard__operator__name='МТС').filter(human__id='151').count()
    symb_mega = HumanSimPresence.objects.filter(simcard__operator__name='Мегафон').filter(human__id='151').count()
    symb_sim2m = HumanSimPresence.objects.filter(simcard__operator__name='СИМ2М').filter(human__id='151').count()

    malash_2011 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2011').filter(human__id='154').count()
    malash_2013 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2013').filter(human__id='154').count()
    malash_2421 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2421').filter(human__id='154').count()
    malash_2423 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2423').filter(human__id='154').count()
    malash_2425 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2425').filter(human__id='154').count()
    malash_2435 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2435').filter(human__id='154').count()
    malash_2437 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2437').filter(human__id='154').count()
    malash_333 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM333').filter(human__id='154').count()
    malash_007 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM007 BLE в прикуриватель').filter(human__id='154').count()
    malash_invis_duos = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos').filter(human__id='154').count()
    malash_invis_duos_s = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos S').filter(human__id='154').count()
    malash_invis_duos_3d_l = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos 3D L').filter(human__id='154').count()
    malash_mts = HumanSimPresence.objects.filter(simcard__operator__name='МТС').filter(human__id='154').count()
    malash_mega = HumanSimPresence.objects.filter(simcard__operator__name='Мегафон').filter(human__id='154').count()
    malash_sim2m = HumanSimPresence.objects.filter(simcard__operator__name='СИМ2М').filter(human__id='154').count()

    leht_2011 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2011').filter(human__id='152').count()
    leht_2013 = HumanTerminalPresence.objects.filter(terminal__model__model='Start S-2013').filter(human__id='152').count()
    leht_2421 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2421').filter(human__id='152').count()
    leht_2423 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2423').filter(human__id='152').count()
    leht_2425 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2425').filter(human__id='152').count()
    leht_2435 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2435').filter(human__id='152').count()
    leht_2437 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2437').filter(human__id='152').count()
    leht_333 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM333').filter(human__id='152').count()
    leht_007 = HumanTerminalPresence.objects.filter(terminal__model__model='ADM007 BLE в прикуриватель').filter(human__id='152').count()
    leht_invis_duos = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos').filter(human__id='152').count()
    leht_invis_duos_s = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos S').filter(human__id='152').count()
    leht_invis_duos_3d_l = HumanTerminalPresence.objects.filter(terminal__model__model='Invis Duos 3D L').filter(human__id='152').count()
    leht_mts = HumanSimPresence.objects.filter(simcard__operator__name='МТС').filter(human__id='152').count()
    leht_mega = HumanSimPresence.objects.filter(simcard__operator__name='Мегафон').filter(human__id='152').count()
    leht_sim2m = HumanSimPresence.objects.filter(simcard__operator__name='СИМ2М').filter(human__id='152').count()

    yar_2420 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2420').filter(human__id='501').count()
    yar_2421 = HumanTerminalPresence.objects.filter(terminal__model__model='Smart S-2421').filter(human__id='501').count()

#    mersl_mts = HumanSimPresence.objects.filter(simcard__operator__name='МТС').filter(human__id='673').count()
#    mersl_mega = HumanSimPresence.objects.filter(simcard__operator__name='Мегафон').filter(human__id='673').count()

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
#        'mersl_mts': mersl_mts,
#        'mersl_mega': mersl_mega

    }
    return render(request, 'general_app/reserve.html', context=context)
