import csv

from django.core.management.base import BaseCommand

from general_app.models import OperatorsSim, SimCards


class Command(BaseCommand):
    help = 'Проверка Симкарт Мегафон по колличеству'

    def handle(self, *args, **options):
        path = 'general_app/management/commands/mega.csv'
        with open(path, 'r', newline='', encoding='latin-1') as data:
            result = csv.DictReader(data, delimiter=';')
            operator = OperatorsSim.objects.get(name='Мегафон')
            sum_sim_list = SimCards.objects.filter(operator=operator).count()
            all_site = 0
            for line in result:
                all_site += 1
            difference = all_site - sum_sim_list
            print(f'На сайте {all_site}, на проекте {sum_sim_list}, разница {difference} шт.')
