from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from .models import (Human, SimCards, Terminals, WialonObject,
                     WialonObjectActive, WialonUser)


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
    user_list = WialonUser.objects.filter(human=None)
    wia_obj_list = WialonObject.objects.filter(wialonobjectactive__isnull=True)
    context = {
        'sim_list': sim_list,
        'term_list': term_list,
        'user_list': user_list,
        'wia_obj_list': wia_obj_list,
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
