import datetime

from django.db import models
from django.utils import timezone as tz


class HumanNames(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Имя'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Имя'
        verbose_name_plural = 'Имена'


class Human(models.Model):
    name_id = models.ForeignKey(
        HumanNames,
        on_delete=models.PROTECT,
        related_name='name_humans',
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия'
    )
    description = models.CharField(
        max_length=128,
        verbose_name='Описание',
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s %s' % (self.name_id, self.last_name)

    class Meta:
        ordering = ['name_id', 'last_name']
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'


class Contact(models.Model):
    name = models.CharField(
        max_length=45,
        verbose_name='Название контакта'
    )
    record = models.ManyToManyField(
        Human,
        through='HumanContact',
        verbose_name='Человек'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Вариант контакта'
        verbose_name_plural = 'Варианты контактов'


class HumanContact(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.CASCADE,
        verbose_name='Человек'
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name='Версия контакта'
    )
    contact_rec = models.CharField(
        max_length=255,
        verbose_name='Запись'
    )

    def __str__(self):
        return self.contact_rec

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class BrandTerminals(models.Model):
    brand = models.CharField(
        max_length=20,
        null=True,
        unique=True,
        verbose_name='Название'
    )

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ['brand']
        verbose_name = 'Марка терминала'
        verbose_name_plural = 'Терминал: марки'


class ModelTerminals(models.Model):
    brand = models.ForeignKey(
        BrandTerminals,
        on_delete=models.PROTECT,
        related_name='brand_models',
        verbose_name='Марка'
    )
    model = models.CharField(
        max_length=20,
        null=True,
        unique=True,
        verbose_name='Модель'
    )

    def __str__(self):
        return '%s %s' % (self.brand, self.model)

    class Meta:
        ordering = ['model']
        verbose_name = 'Модель терминала'
        verbose_name_plural = 'Терминал: модели'


class Terminals(models.Model):
    model = models.ForeignKey(
        ModelTerminals,
        on_delete=models.PROTECT,
        related_name='model_terminals',
        verbose_name='Модель',
        null=True,
        blank=True
    )
    serial_number = models.CharField(
        max_length=20,
        verbose_name='Серийный номер',
        null=True,
        blank=True
    )
    imei = models.CharField(
        max_length=20,
        verbose_name='IMEI',
        unique=True,
        null=True,
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Действующий'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    def __str__(self):
        return self.imei

    class Meta:
        ordering = ['imei']
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'


class HumanTerminalPresence(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_terminal_holders',
        verbose_name='Человек'
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
        related_name='terminal_holders',
        verbose_name='Терминал'
    )
    time_create = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата'
    )

    class Meta:
        ordering = ['human']
        verbose_name = 'Человек + Терминал'
        verbose_name_plural = 'Люди + Терминалы'


class Sensors(models.Model):
    model = models.ForeignKey(
        ModelTerminals,
        on_delete=models.PROTECT,
        related_name='model_sensors',
        verbose_name='Модель'
    )
    serial_number = models.CharField(
        max_length=255,
        verbose_name='Серийный номер',
        blank=True,
        null=True
    )
    add_information = models.CharField(
        max_length=255,
        verbose_name='Доп.инфо',
        blank=True,
        null=True,
    )
    comment = models.CharField(
        max_length=255,
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )
    time_create = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return '%s %s' % (self.model, self.serial_number)

    class Meta:
        ordering = ['serial_number']
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'


class HumanSensorRelations(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_sensor_holders',
        verbose_name='Человек'
    )
    sensor = models.OneToOneField(
        Sensors,
        on_delete=models.PROTECT,
        related_name='sensor_holders',
        verbose_name='Датчик'
    )
    comment = models.CharField(
        max_length=255,
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )
    time_create = models.DateField(
        auto_now=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['human']
        verbose_name = 'Человек + Датчик'
        verbose_name_plural = 'Люди + Датчики'


class OperatorsSim(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Название',
        null=True,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'


class SimCards(models.Model):
    operator = models.ForeignKey(
        OperatorsSim,
        on_delete=models.PROTECT,
        related_name='operator_sim_cards',
        verbose_name='Оператор'
    )
    number = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Номер'
    )
    icc = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='ICC'
    )
    terminal = models.ForeignKey(
        Terminals,
        on_delete=models.PROTECT,
        related_name='terminal_sim_cards',
        verbose_name='Терминал',
        null=True,
        blank=True
    )
    personal = models.BooleanField(
        default=False,
        verbose_name='Личная'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.icc

    class Meta:
        ordering = ['number']
        verbose_name = 'SIM-карта'
        verbose_name_plural = 'SIM-карты'


class HumanSimPresence(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_sim_card_holders',
        verbose_name='Человек'
    )
    simcard = models.OneToOneField(
        SimCards,
        on_delete=models.PROTECT,
        related_name='sim_card_holders',
        verbose_name='SIM-карта'
    )
    time_create = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата'
    )

    class Meta:
        ordering = ['human']
        verbose_name = 'Человек + SIM-карта'
        verbose_name_plural = 'Люди + SIM-карты'


class WialonServer(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Сервер'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Сервер'
        verbose_name_plural = 'Серверы'


class WialonUser(models.Model):
    server = models.ForeignKey(
        WialonServer,
        on_delete=models.PROTECT,
        related_name='server_glonass_users',
        verbose_name='Сервер',
    )
    user_name = models.CharField(
        max_length=255,
        verbose_name='Учётная запись'
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_glonass_users',
        verbose_name='Человек',
        null=True,
        blank=True
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['user_name']
        verbose_name = 'Учётная запись'
        verbose_name_plural = 'Учётные записи'


class WialonObject(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Имя',
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
        related_name='terminal_glonass_objects',
        verbose_name='Терминал',
        null=True,
        blank=True
    )
    wialon_user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='user_glonass_objects',
        verbose_name='Учётная запись',
    )
    price = models.PositiveBigIntegerField(
        default=1,
        verbose_name='Цена'
    )
    payer = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='payer_glonass_objects',
        verbose_name='Плательщик'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Нужность'
    )
    date_change_status = models.DateField(
        verbose_name='Дата оплаты',
        null=True,
        blank=True
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def save(self, *args, **kwargs):
        HumanTerminalPresence.objects.filter(
                terminal=self.terminal
        ).delete()
        super(WialonObject, self).save(*args, **kwargs)


class UserWialonServer(models.Model):
    user = models.OneToOneField(
        WialonUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    server = models.ForeignKey(
        WialonServer,
        on_delete=models.PROTECT,
        related_name='userwialonservers',
        verbose_name='Сервер',
        null=True,
        blank=True,
    )

    def __str__(self):
        return '%s %s' % (self.user, self.server)

    class Meta:
        ordering = ['user']
        verbose_name = 'Сервер + Пользователь'
        verbose_name_plural = 'Серверы + Пользователи'


class BrandCar(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название Марки'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Марка ТС'
        verbose_name_plural = 'ТС: марки'


class ModelCar(models.Model):
    brand = models.ForeignKey(
        BrandCar,
        on_delete=models.PROTECT,
        related_name='brand_car_models',
        verbose_name='Марка'
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Модель'
    )

    def __str__(self):
        return '%s %s' % (self.brand, self.name)

    class Meta:
        ordering = ['brand']
        verbose_name = 'Модель ТС'
        verbose_name_plural = 'ТС: модели'


class CarGenerations(models.Model):
    model_id = models.ForeignKey(
        ModelCar,
        on_delete=models.PROTECT,
        related_name='model_car_generations',
        verbose_name='Модель'
    )
    generation = models.CharField(
        max_length=128,
        verbose_name='Поколение'
    )
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return '%s %s' % (self.model_id, self.generation)

    class Meta:
        ordering = ['model_id']
        verbose_name = 'Поколение ТС'
        verbose_name_plural = 'ТС: поколения'


class Installation(models.Model):
    date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата'
    )
    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Место'
    )
    model = models.ForeignKey(
        ModelCar,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='model_installations',
        verbose_name='Модель ТС'
    )
    vin = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        verbose_name='VIN'
    )
    state_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Гос. номер'
    )
    terminal = models.ForeignKey(
        Terminals,
        on_delete=models.PROTECT,
        related_name='terminal_installations',
        verbose_name='Терминал'
    )
    human_worker = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_worker_installations',
        verbose_name='Установщик'
    )
    user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='user_installations',
        verbose_name='Пользователь'
    )
    juristic_person = models.BooleanField(
        verbose_name='Юр-лицо'
    )
    payer = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='payer_installations',
        verbose_name='Плательщик'
    )
    payment = models.BooleanField(
        default=False,
        verbose_name='Оплата'
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )

    def __str__(self):
        return str(self.terminal)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Установка'
        verbose_name_plural = 'Установки'


class Schedules(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='human_schedules',
        verbose_name='Человек'
    )
    date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата'
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )

    def __str__(self):
        return '%s %s' % (self.human, self.date)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Смена'
        verbose_name_plural = 'График'


class PriceLogistics(models.Model):
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Пункт'
    )
    cost = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Цена'
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    last_modified = models.DateField(
        auto_now=True,
        verbose_name='Посл. изменения'
    )

    def __str__(self):
        return '%s %s' % (self.city, self.cost)

    class Meta:
        ordering = ['city']
        verbose_name = 'Выезд'
        verbose_name_plural = 'Прайс.Выезды'


class PriceTrackers(models.Model):
    tracker_model = models.ForeignKey(
        ModelTerminals,
        on_delete=models.PROTECT,
        related_name='model_tracker_prices',
        verbose_name='Модель трекера'
    )
    cost = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Цена'
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    last_modified = models.DateField(
        auto_now=True,
        verbose_name='Посл. изменения'
    )

    def __str__(self):
        return '%s %s' % (self.tracker_model, self.cost)

    class Meta:
        ordering = ['cost']
        verbose_name = 'Цена'
        verbose_name_plural = 'Прайс.Оборудование'


class Services(models.Model):
    service = models.CharField(
        max_length=255,
        verbose_name='Услуга'
    )
    cost = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Цена'
    )
    ordering = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Очерёдность'
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    last_modified = models.DateField(
        auto_now=True,
        verbose_name='Посл. изменения'
    )

    def __str__(self):
        return self.service

    class Meta:
        ordering = ['ordering', 'service']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
