from django.shortcuts import render
from .models import Human, SimCards, Terminals, WialonObject, WialonUser
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q


@login_required
def index_view(request):
    sim_list = SimCards.objects.filter(terminal=None)
    term_all = Terminals.objects.all()
    term_list = []
    for i in term_all:
        if not WialonObject.objects.filter(terminal=i).exists():
            term_list.append(i)
    user_list = WialonUser.objects.filter(human=None)

#    wialin_obj_all = Count('wialonuser__wialonobject')
#    wialin_obj_active = Count(
#        'wialonuser__wialonobject__wialonobjectactive',
#        filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
#    )
#    client_list = Human.objects.annotate(all=wialin_obj_all).annotate(active=wialin_obj_active)

    context = {
        'sim_list': sim_list,
        'term_list': term_list,
        'user_list': user_list
#        'client_list': client_list
    }
    return render(request, 'general_app/index.html', context=context)
