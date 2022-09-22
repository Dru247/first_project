from django.db import models
from django.utils import timezone as tz
from django.core.exceptions import ValidationError


class Human(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name']


class Contact(models.Model):
    name = models.CharField(max_length=45)
    record = models.ManyToManyField(
        Human,
        through='HumanContact'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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
        unique=True
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
    )
    model = models.CharField(
        max_length=20,
        null=True,
        unique=True
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
        null=True,
        blank=True
    )
    serial_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    imei = models.CharField(
        max_length=20,
        unique=True,
        null=True,
    )
    time_create = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.imei)

    class Meta:
        ordering = ['imei']
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'


class HumanTerminalPresence(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        null=True,
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
    )
    time_create = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['human']
        verbose_name = 'Человек + Терминал'
        verbose_name_plural = 'Люди + Терминалы'


class OperatorsSim(models.Model):
    name = models.CharField(
        max_length=20,
        null=True,
        unique=True
    )

    def __str__(self):
        return self.name


class SimCards(models.Model):
    operator = models.ForeignKey(
        OperatorsSim,
        on_delete=models.PROTECT,
        related_name='s_operator',
        null=True
    )
    number = models.CharField(
        max_length=16,
        null=True,
        unique=True
    )
    icc = models.CharField(
        max_length=20,
        null=True,
        unique=True
    )
    terminal = models.ForeignKey(
        Terminals,
        on_delete=models.PROTECT,
        related_name='s_terminal',
        null=True,
        blank=True
    )
    time_create = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = 'Сим-карта'
        verbose_name_plural = 'Сим-карты'


class HumanSimPresence(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        related_name='humansimpresences'
    )
    simcard = models.OneToOneField(
        SimCards,
        on_delete=models.PROTECT,
        related_name='humansimpresences'
    )
    time_create = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['human']
        verbose_name = 'Человек + Симка'
        verbose_name_plural = 'Люди + Симки'


class WialonUser(models.Model):
    user_name = models.CharField(
        max_length=20,
        unique=True
    )
    password = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['user_name']


class WialonObject(models.Model):
    name = models.CharField(max_length=45)
    wialon_user = models.ForeignKey(
        WialonUser,
        on_delete=models.PROTECT,
        related_name='wialonobjects',
        null=True,
        blank=True
    )
    terminal = models.OneToOneField(
        Terminals,
        on_delete=models.PROTECT,
        related_name='wialonobjects'
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        HumanTerminalPresence.objects.filter(
                terminal=self.terminal
        ).delete()
        super(WialonObject, self).save(*args, **kwargs)


class WialonObjectActive(models.Model):
    wialon_object = models.OneToOneField(
        WialonObject,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(default=tz.now)

    def __str__(self):
        return str(self.wialon_object)

    class Meta:
        ordering = ['wialon_object']


class WialonServer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserWialonServer(models.Model):
    user = models.OneToOneField(
        WialonUser,
        on_delete=models.CASCADE,
    )
    server = models.ForeignKey(
        WialonServer,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )


class Company(models.Model):
    name = models.CharField(
        max_length=45,
        verbose_name='Название'
    )
    human_company = models.ManyToManyField(
        Human,
        through='HumanCompany'
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
        verbose_name='Юзер'
    )

    class Meta:
        verbose_name = 'Компания + Юзер'
        verbose_name_plural = 'Компании + Юзеры'
