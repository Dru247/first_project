from django.shortcuts import render
from .models import Human, SimCards, Terminals, WialonObject, WialonUser, WialonObjectActive
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q


@login_required
def index_view(request):
    sim_list = SimCards.objects.filter(terminal=None, humansimpresence__isnull=True)
    term_all = Terminals.objects.all()
    term_list = []
    for i in term_all:
        if not WialonObject.objects.filter(terminal=i).exists():
            term_list.append(i)
    user_list = WialonUser.objects.filter(human=None)
    context = {
        'sim_list': sim_list,
        'term_list': term_list,
        'user_list': user_list
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
    client_list = Human.objects.annotate(all=wialon_obj_all).annotate(active=wialon_obj_active)
    context = {
        'client_list': client_list,
        'activ_obj_all': activ_obj_all,
        'not_activ_obj_all': not_activ_obj_all,
    }
    return render(request, 'general_app/clients.html', context=context)
