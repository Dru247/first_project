import csv

from django.core.management.base import BaseCommand

from general_app.models import Human, HumanSimPresence, OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Занесение симкарт Мегафон в базу'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mega.csv'
        with open(path, 'r', newline='') as data:
            result = csv.DictReader(data, delimiter=',')
            operator = OperatorsSim.objects.get(name='Мегафон')
            human = Human.objects.get(last_name='Лехтин')
            for line in result:
                number = line['number']
                icc = line['icc']
                SimCards.objects.get_or_create(
                    operator=operator,
                    number=number,
                    icc=icc
                )
                sim = SimCards.objects.get(number=number)
                if not sim.terminal and not HumanSimPresence.objects.filter(simcard=sim).exists():
                    HumanSimPresence.objects.get_or_create(
                        human=human,
                        simcard=sim
                    )
