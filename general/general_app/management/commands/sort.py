import csv
from general_app.models import SimCards, OperatorsSim, HumanTerminalPresence, WialonServer, Terminals, Human, TelephoneNumber, UserWialonServer, Telegram, WialonUser, WialonObject, WialonObjectActive
from django.core.management.base import BaseCommand
import time
from django.core.files.base import File
from django.db.models import Count
from django.db.models import Q


class Command(BaseCommand):
    help = 'Сортировка'

    def handle(self, *args, **options):
#        term_all = Terminals.objects.all()
#        sim_list_2 = []
#        for i in term_all:
#            if not WialonObject.objects.filter(terminal=i).exists():
#                sim_list_2.append(i)
#        print(len(sim_list_2))

        path = 'general_app/management/commands/list_47.csv'
        with open(path, 'r', newline='') as data:
            result = csv.DictReader(data, delimiter=',')
            list_y4 = []
            for line in result:
                a = line['ID']
                b = line['last_n']
                x = Terminals.objects.get(imei=a)
                y = Human.objects.get(last_name=b)
                HumanTerminalPresence.objects.get_or_create(human=y, terminal=x)


#                if x not in list_y4:
#                    list_y4.append(x)
#            for r in list_y4:
#                WialonUser.objects.get_or_create(user_name=r)
#                time.sleep(0.5)
#                m = WialonServer.objects.get(name='COM')
#                UserWialonServer.objects.create(
#                    user=WialonUser.objects.get(user_name=r),
#                    server=m
#                )
#                t = Terminals.objects.get(imei=y)
#                WialonObject.objects.get_or_create(
#                    name=i,
#                    wialon_user=WialonUser.objects.get(user_name=x),
#                    terminal=t,
#                )
#                WialonObjectActive.objects.get_or_create(
#                    wialon_object=WialonObject.objects.get(terminal=t)
#                )


#                a = WialonUser.objects.get(user_name=x)
#                b = Terminals.objects.get(imei=y)
#                WialonObject.objects.create(
#                    name=i,
#                    wialon_user=a,
#                    terminal=b
#                )

#        wialin_obj_all = Count('wialonuser__wialonobject')
#        wialin_obj_active = Count(
#            'wialonuser__wialonobject__wialonobjectactive',
#            filter=Q(wialonuser__wialonobject__wialonobjectactive__active=True)
#        )
#        a = Human.objects.annotate(all=wialin_obj_all).annotate(active=wialin_obj_active)
#        for i in a:
#            y = i.all
#            z = i.active
#            print(i, y, z, y*350)

#        wia = WialonUser.objects.all()
#        serv = WialonServer.objects.get(name='RU')
#        for i in wia:
#            UserWialonServer.objects.create(
#                user=i,
#                server=serv
#            )
