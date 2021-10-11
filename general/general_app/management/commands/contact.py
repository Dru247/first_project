from django.core.management.base import BaseCommand

from general_app.models import Human, Contact, HumanContact, TelephoneNumber, Telegram


class Command(BaseCommand):
    help = 'Перенос контактов'

    def handle(self, *args, **options):
        con_list = ('Email', 'Telegram', 'Номер телефона')
        for i in con_list:
            Contact.objects.get_or_create(
                name=i
            )
        tele_all = TelephoneNumber.objects.all()
        for result in tele_all:
            hum = Human.objects.get(id=result.human.id)
            HumanContact.objects.get_or_create(
                human=hum,
                contact=Contact.objects.get(name='Номер телефона'),
                contact_rec=result.number
            )
        teleg_all = Telegram.objects.all()
        for result in teleg_all:
            hum = Human.objects.get(id=result.human.id)
            HumanContact.objects.get_or_create(
                human=hum,
                contact=Contact.objects.get(name='Telegram'),
                contact_rec=result.telegram_id
            )
