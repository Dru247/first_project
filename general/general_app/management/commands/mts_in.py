import csv

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from general_app.models import Human, HumanSimPresence, OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Занесение симкарт МТС в базу'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mts.csv'
        with open(path, 'r', newline='') as data:
            operator = OperatorsSim.objects.get(name='МТС')
            human = Human.objects.get(last_name='Лехтин')
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                number = line['number'][1:]
                icc = line['icc']
                SimCards.objects.get_or_create(
                    operator=operator,
                    number=number,
                    icc=icc
                )
                sim = SimCards.objects.get(icc=icc)
                if not sim.terminal and not HumanSimPresence.objects.filter(simcard=sim).exists():
                    HumanSimPresence.objects.get_or_create(
                        human=human,
                        simcard=sim
                    )
