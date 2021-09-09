import csv
from general_app.models import SimCards, OperatorsSim, Terminals, Human, TelephoneNumber, Telegram, WialonUser, WialonObject, WialonObjectActive
from django.core.management.base import BaseCommand
import time
from django.core.files.base import File
from django.db.models import Count
from django.db.models import Q


class Command(BaseCommand):
    help = 'Сортировка'

    def handle(self, *args, **options):
#        path = 'general_app/management/commands/t_3_s.csv'
#        with open(path, 'r', newline='') as data:
#            result = csv.DictReader(data, delimiter=',')
#            for line in result:
#                i = line['Имя']
#                x = line['Учетная запись']
#                y = line['ID']
#                a = WialonUser.objects.get(user_name=x)
#                b = Terminals.objects.get(imei=y)
#                WialonObject.objects.create(
#                    name=i,
#                    wialon_user=a,
#                    terminal=b
#                )
        wialin_obj_all = Count('wialonuser__wialonobject')
        wialin_obj_active = Count(
            'wialonuser__wialonobject__wialonobjectactive',
            filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
        )
        a = Human.objects.annotate(all=wialin_obj_all).annotate(active=wialin_obj_active)
        for i in a:
            y = i.all
            z = i.active
            print(i, y, z, y*350)
