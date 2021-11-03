import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from general_app.models import (Human, HumanSimPresence, HumanTerminalPresence,
                                ModelTerminals, SimCards, Terminals, WialonObject)


class Command(BaseCommand):
    help = 'Занесение терминалов в базу'

    def handle(self, *args, **options):
        brand_list = {
            '2425': ModelTerminals.objects.get(model='Smart S-2425'),
            '2435': ModelTerminals.objects.get(model='Smart S-2435')
        }
        path = 'general_app/management/commands/term.csv'
        with open(path, 'r', newline='') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                model = line['model']
                imei = line['imei']
                sn = line['sn']
                icc_1 = line['icc_1']
                icc_2 = line['icc_2']
                human = line['human']
                Terminals.objects.get_or_create(
                    model=brand_list[model],
                    serial_number=sn,
                    imei=imei
                )
                sim_now = SimCards.objects.filter(icc__in=[icc_1, icc_2])
                print(len(sim_now))
                term = Terminals.objects.get(imei=imei)
                for sim in sim_now:
                    SimCards.objects.filter(icc=sim.icc).update(terminal=term)
                    try:
                        HumanSimPresence.objects.get(simcard=sim).delete()
                    except ObjectDoesNotExist:
                        print(f'{sim} отсутствует у Лехтина')
                human_now = Human.objects.get(last_name=human)
                if not WialonObject.objects.filter(terminal=term).exists():
                    HumanTerminalPresence.objects.get_or_create(
                        human=human_now,
                        terminal=term
                    )
