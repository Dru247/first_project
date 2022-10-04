from django.db import models
from django.utils import timezone as tz
from django.core.exceptions import ValidationError

import datetime


class Human(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name']
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
        max_length=45,
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
        verbose_name_plural = 'Марки терминалов'


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
        verbose_name_plural = 'Модели терминалов'


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
        verbose_name='Дата'
    )

    def __str__(self):
        return self.number

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


class WialonUser(models.Model):
    user_name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Пользователь'
    )
    password = models.CharField(
        max_length=20,
        verbose_name='Пароль',
        null=True,
        blank=True
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        verbose_name='Человек',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['user_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class WialonObject(models.Model):
    name = models.CharField(max_length=45)
    wialon_user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='wialonobjects',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
        related_name='wialonobjects',
        verbose_name='Терминал',
        null=True,
        blank=True
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
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
        verbose_name = 'Пользователь + Сервер'
        verbose_name_plural = 'Пользователи + Серверы'


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
        verbose_name_plural = 'Марки ТС'


class ModelCar(models.Model):
    brand = models.ForeignKey(
        BrandCar,
        on_delete=models.PROTECT,
        related_name='modelcars',
        verbose_name='Марка ТС'
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Название Модели'
    )

    def __str__(self):
        return '%s %s' % (self.brand, self.name)


    class Meta:
        ordering = ['brand']
        verbose_name = 'Модель ТС'
        verbose_name_plural = 'Модели ТС'


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
    payment = models.BooleanField(
        default=False,
        verbose_name='Оплата'
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
