from django.shortcuts import render
from .models import Human
from django.db.models import Count, Q


def clients_view(request):
    wialin_obj_all = Count('wialonuser__wialonobject')
    wialin_obj_active = Count(
        'wialonuser__wialonobject__wialonobjectactive',
        filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
    )
    client_list = Human.objects.annotate(all=wialin_obj_all).annotate(active=wialin_obj_active)

    context = {
        'client_list': client_list
    }
    return render(request, '', context=context)
