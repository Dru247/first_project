import csv

from django.core.management.base import BaseCommand

from general_app.models import OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Проверка Симкарт МТС по колличеству, между Проектои и сайтом' \
           ', с выводом недостающих симкарт в cvs'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mts.csv'
        path_2 = 'general_app/management/commands/mts_out.csv'
        write = open(path_2, 'w', newline='', encoding='utf-8')
        fieldnames = [
                'Наименование устройства',
                'Идентификационный номер',
                'Тип устройства',
                'Номер телефона',
                'Адрес, где находится устройство'
            ]
        writer = csv.DictWriter(write, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        with open(path, 'r', newline='', encoding='utf-8-sig') as data:
            result = csv.DictReader(data, delimiter=';')
            operator = OperatorsSim.objects.get(name='МТС')
            sim_project = SimCards.objects.filter(operator=operator)
            icc_website = []
            for line in result:
                number = line['Абонентский номер'][1:]
                icc = line['Номер SIM-карты'].strip()
                icc_website.append(icc)
                if SimCards.objects.filter(icc=icc).exists():
                    pass
                else:
                    print(f'{number}, {icc} - на МТС есть, на проекте нет')
                    writer.writerow({fieldnames[2]: 'Устройство ГЛОНАСС', fieldnames[3]: number})
            for sim in sim_project:
                if sim.icc not in icc_website:
                    print(f'{sim.number}, {sim.icc} - на проекте есть, на МТС нет')
        write.close()
