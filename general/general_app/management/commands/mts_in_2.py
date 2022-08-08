import csv

from django.core.management.base import BaseCommand

from general_app.models import Human, HumanSimPresence, OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Занесение симкарт МТС на проект'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mts.csv'
        with open(path, 'r', newline='', encoding='utf-8-sig') as data:
            operator = OperatorsSim.objects.get(name='МТС')
            human = Human.objects.get(pk=input('Введите ID человека, на которого нужно внести симки > '))
            result = csv.DictReader(data, delimiter=';')
            for line in result:
                number = line['Абонентский номер'][1:]
                icc = line['Номер SIM-карты'].strip()
                if SimCards.objects.filter(number=number).exists():
                    pass
                else:
                    SimCards.objects.create(
                        operator=operator,
                        number=number,
                        icc=icc
                    )
                    sim = SimCards.objects.get(icc=icc)
                    HumanSimPresence.objects.create(
                        human=human,
                        simcard=sim
                    )
