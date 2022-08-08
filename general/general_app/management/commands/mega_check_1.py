import csv

from django.core.management.base import BaseCommand

from general_app.models import Human, HumanSimPresence, OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Проверка Симкарт Мегафон по колличеству, между Проектом и сайтом' \
           ', с выводом недостающих симкарт в cvs'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mega.csv'
        path_1 = 'general_app/management/commands/mega_out.csv'
        path_2 = 'general_app/management/commands/mega_for-roaming.csv'

        write_1 = open(path_1, 'w', newline='', encoding='utf-8')
        fieldnames = [
                'Наименование устройства',
                'Идентификационный номер',
                'Тип устройства',
                'Номер телефона',
                'Адрес, где находится устройство'
        ]
        writer_1 = csv.DictWriter(write_1, fieldnames=fieldnames, delimiter=';')
        writer_1.writeheader()
        write_2 = open(path_2, 'w', newline='', encoding='utf-8')
        writer_2 = csv.writer(write_2, delimiter=';')
        with open(path, 'r', newline='', encoding='cp1251') as data:
            result = csv.DictReader(data, delimiter=';')
            operator = OperatorsSim.objects.get(name='Мегафон')
            sim_project = SimCards.objects.filter(operator=operator)
            icc_website = []
            for line in result:
                number = line['Номер']
                icc = line['ICC']
                icc_website.append(icc)
                if SimCards.objects.filter(icc=icc).exists():
                    pass
                else:
                    print(f'{number}, {icc} - на Мегафон есть, на проекте нет')
                    writer_1.writerow({fieldnames[2]: 'Устройство ГЛОНАСС', fieldnames[3]: number})
                    writer_2.writerow([number, icc])
            for sim in sim_project:
                if sim.icc not in icc_website:
                    print(f'{sim.number}, {sim.icc} - на проекте есть, на Мегафон нет')
        write_1.close()
        write_2.close()

