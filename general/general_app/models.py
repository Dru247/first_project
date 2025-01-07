import datetime

# from audioop import minmax
from django.db import models
from django.utils import timezone as tz
# from django.core.exceptions import ValidationError


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


class TelephoneNumber(models.Model):
    """Пока не нужна"""
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
    )
    number = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return str(self.number)


class Telegram(models.Model):
    """Пока не нужна"""
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT
    )
    telegram_id = models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return str(self.telegram_id)


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
        related_name='models',
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
        related_name='t_model',
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
        related_name='humanterminalpresences',
        verbose_name='Человек'
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
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
        related_name='s_operator',
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
        related_name='s_terminal',
        verbose_name='Терминал',
        null=True,
        blank=True
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
        related_name='humansimpresences',
        verbose_name='Человек'
    )
    simcard = models.OneToOneField(
        SimCards,
        on_delete=models.PROTECT,
        related_name='humansimpresences',
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
        verbose_name='Сервер',
    )
    user_name = models.CharField(
        max_length=255,
        verbose_name='Учётная запись'
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
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
        related_name='wialonobjects',
        verbose_name='Терминал',
        null=True,
        blank=True
    )
    wialon_user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='wialonobjects',
        verbose_name='Учётная запись',
    )
    price = models.PositiveBigIntegerField(
        default=1,
        verbose_name='Цена'
    )
    payer = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='payer_human',
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


# Нужно удалить
class WialonObjectActive(models.Model):
    wialon_object = models.OneToOneField(
        WialonObject,
        on_delete=models.CASCADE,
        verbose_name='Объект'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Статус'
    )
    last_modified = models.DateTimeField(
        default=tz.now,
        verbose_name='Дата'
    )

    def __str__(self):
        return str(self.wialon_object)

    class Meta:
        ordering = ['wialon_object']
        verbose_name = 'Объект + Статус'
        verbose_name_plural = 'Объекты + Статусы'


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


class Company(models.Model):
    name = models.CharField(
        max_length=45,
        verbose_name='Название'
    )
    human_company = models.ManyToManyField(
        Human,
        through='HumanCompany',
        verbose_name='Человек'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class HumanCompany(models.Model):
    company_hum = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        verbose_name='Компания'
    )
    human_comp = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        verbose_name='Человек'
    )

    class Meta:
        verbose_name = 'Компания + Человек'
        verbose_name_plural = 'Компании + Люди'


class UserCompany(models.Model):
    company_us = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        verbose_name='Компания'
    )
    user_comp = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Компания + Пользователь'
        verbose_name_plural = 'Компании + Пользователи'


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
        related_name='modelcars',
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
        related_name='installations',
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
        related_name='installations',
        verbose_name='Терминал'
    )
    human_worker = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='installations',
        verbose_name='Установщик'
    )
    user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='installations',
        verbose_name='Пользователь'
    )
    juristic_person = models.BooleanField(
        verbose_name='Юр-лицо'
    )
    payer = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
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


class InstallationComment(models.Model):
    installation = models.OneToOneField(
        Installation,
        on_delete=models.PROTECT,
        related_name='installationcomments',
        verbose_name='Установка'
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Текст'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['installation']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Установки + Комментарии'


class Schedules(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
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

    def __str__(self):
        return '%s %s' % (self.city, self.cost)

    class Meta:
        ordering = ['city']
        verbose_name = 'Выезд'
        verbose_name_plural = 'Цена выездов'
