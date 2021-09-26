import csv
import time

from django.core.files.base import File
from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from general_app.models import (Human, HumanSimPresence, HumanTerminalPresence,
                                OperatorsSim, SimCards, Telegram,
                                TelephoneNumber, Terminals, UserWialonServer,
                                WialonObject, WialonObjectActive, WialonServer,
                                WialonUser)


class Command(BaseCommand):
    help = 'Сортировка'

    def handle(self, *args, **options):
        """Загрузка новых симкарт(чек - result, x,)"""
        path = 'general_app/management/commands/mega.csv'
        with open(path, 'r', newline='') as data:
            result = csv.DictReader(data, delimiter=';')
            x = OperatorsSim.objects.get(name='Мегафон')
            y = Human.objects.get(last_name='Лехтин')
            for line in result:
                a = line['number']
                b = line['ICC']
#                c = line['Operator']
                if SimCards.objects.filter(number=a).exists():
                    pass
                else:
                    SimCards.objects.get_or_create(
                        operator=x,
                        number=a,
                        icc=b
                    )
                    z = SimCards.objects.get(number=a)
                    HumanSimPresence.objects.get_or_create(
                        human=y,
                        simcard=z
                    )


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
#        a = Human.objects.annotate(all=wialin_obj_all). \
#            annotate(active=wialin_obj_active)
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
