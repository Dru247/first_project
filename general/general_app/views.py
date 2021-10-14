import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.db.models import Max

from .models import (Human, SimCards, Terminals, WialonObject,
                     WialonObjectActive, WialonUser, WialonServer, Company, UserCompany)


@login_required
def index_view(request):
    sim_list = SimCards.objects.filter(
        terminal=None,
        humansimpresence__isnull=True
    )
    term_list = Terminals.objects.filter(
        wialonobject__isnull=True,
        humanterminalpresence__isnull=True
    )
    user_company_list = UserCompany.objects.all()
    user_list = WialonUser.objects.filter(human=None).exclude(usercompany__in=user_company_list)
    wia_obj_list = WialonObject.objects.filter(wialonobjectactive__isnull=True)
    sum_wia_obj_serv_active = Count(
        'userwialonserver__user__wialonobject__wialonobjectactive',
        filter=Q(userwialonserver__user__wialonobject__wialonobjectactive__active=True)
    )
    wia_obj_serv_active = WialonServer.objects.annotate(active=sum_wia_obj_serv_active)
    user_not_serv = WialonUser.objects.filter(userwialonserver__isnull=True)
    context = {
        'sim_list': sim_list,
        'term_list': term_list,
        'user_list': user_list,
        'wia_obj_list': wia_obj_list,
        'wia_obj_serv_active': wia_obj_serv_active,
        'user_not_serv': user_not_serv
    }
    return render(request, 'general_app/index.html', context=context)


@login_required
def clients_view(request):
    activ_obj_all = len(WialonObjectActive.objects.filter(active=True))
    not_activ_obj_all = len(WialonObjectActive.objects.filter(active=False))
    wialon_obj_all = Count('wialonuser__wialonobject')
    wialon_obj_active = Count(
        'wialonuser__wialonobject__wialonobjectactive',
        filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
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
    serv_now = get_object_or_404(WialonServer, pk=server_id)
    a = WialonUser.objects.filter(userwialonserver__server=serv_now).filter(wialonobject__wialonobjectactive__active=True)
    sum_wia_obj_active = Count(
        'wialonuser__wialonobject__wialonobjectactive',
        filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
    )
    human_list_server = Human.objects.filter(wialonuser__in=a).annotate(active=sum_wia_obj_active)
    sum_wia_obj_active_comp = Count(
        'usercompany__user_comp__wialonobject__wialonobjectactive',
        filter=Q(usercompany__user_comp__wialonobject__wialonobjectactive__active=True)
    )
    company_list = Company.objects.filter(usercompany__user_comp__in=a)
    company_list_annot = company_list.annotate(active=sum_wia_obj_active_comp)
    sum_wia_obj_serv_active = Count(
        'userwialonserver__user__wialonobject__wialonobjectactive',
        filter=Q(userwialonserver__user__wialonobject__wialonobjectactive__active=True)
    )
    wia_obj_serv = WialonServer.objects.filter(pk=server_id)
    wia_obj_serv_active = wia_obj_serv.annotate(active=sum_wia_obj_serv_active)
    context = {
        'human_list_server': human_list_server,
        'company_list_annot': company_list_annot,
        'wia_obj_serv_active': wia_obj_serv_active
    }
    return render(request, 'general_app/server.html', context=context)


@login_required
def delete_sim_view(request):
    date_1 = datetime.datetime.now()
    year_now = date_1.year
    month_now_1 = date_1.month
    month_now = date_1.month
    if month_now < 6:
        month_now = date_1.month + 12
    month_delta = month_now - 5
    sim_list = SimCards.objects.filter(
        terminal__wialonobject__wialonobjectactive__last_modified__month__lte=month_now_1,
    ).exclude(
        terminal__wialonobject__wialonobjectactive__last_modified__year=year_now
    ).annotate(
        data_deactivate=Max('terminal__wialonobject__wialonobjectactive__last_modified')
    ).order_by('operator')
    sim_list_deactivate = SimCards.objects.filter(
        terminal__wialonobject__wialonobjectactive__last_modified__month=month_delta,
        operator__name='МТС'
    ).annotate(
        data_deactivate=Max('terminal__wialonobject__wialonobjectactive__last_modified')
    )
    context = {
        'sim_list': sim_list,
        'sim_list_deactivate': sim_list_deactivate
    }
    return render(request, 'general_app/sim_delete.html', context=context)
