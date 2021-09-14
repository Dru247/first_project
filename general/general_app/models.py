from django.db import models


class Human(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class TelephoneNumber(models.Model):
    human = models.ForeignKey(Human,
                              on_delete=models.PROTECT,
                              )
    number = models.CharField(max_length=20,
                              unique=True
                              )

    def __str__(self):
        return str(self.number)


class Telegram(models.Model):
    human = models.ForeignKey(Human,
                              on_delete=models.PROTECT,
                              null=True
                              )
    telegram_id = models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return str(self.telegram_id)


class BrandTerminals(models.Model):
    brand = models.CharField(max_length=20,
                             null=True,
                             unique=True
                             )

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ['brand']


class ModelTerminals(models.Model):
    brand = models.ForeignKey(BrandTerminals,
                              on_delete=models.PROTECT,
                              related_name='t_brand',
                              null=True
                              )
    model = models.CharField(max_length=20,
                             null=True,
                             unique=True
                             )

    def __str__(self):
        return self.model

    class Meta:
        ordering = ['model']


class Terminals(models.Model):
    model = models.ForeignKey(ModelTerminals,
                              on_delete=models.PROTECT,
                              related_name='t_model',
                              null=True,
                              blank=True
                              )
    serial_number = models.CharField(max_length=20,
                                     null=True
                                     )
    imei = models.CharField(max_length=20,
                            unique=True,
                            null=True,
                            )

    def __str__(self):
        return str(self.imei)

    class Meta:
        ordering = ['imei']


class OperatorsSim(models.Model):
    name = models.CharField(max_length=20,
                            null=True,
                            unique=True
                            )

    def __str__(self):
        return self.name


class SimCards(models.Model):
    operator = models.ForeignKey(OperatorsSim,
                                 on_delete=models.PROTECT,
                                 related_name='s_operator',
                                 null=True
                                 )
    number = models.CharField(max_length=20,
                              null=True,
                              unique=True)
    icc = models.CharField(max_length=20,
                           null=True,
                           unique=True
                           )
    terminal = models.ForeignKey(Terminals,
                                 on_delete=models.PROTECT,
                                 related_name='s_terminal',
                                 null=True,
                                 blank=True
                                 )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']


class WialonUser(models.Model):
    user_name = models.CharField(max_length=20,
                                 unique=True
                                 )
    password = models.CharField(max_length=20,
                                null=True,
                                blank=True
                                )
    human = models.ForeignKey(Human,
                              on_delete=models.PROTECT,
                              null=True,
                              blank=True
                              )

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['user_name']


class WialonObject(models.Model):
    name = models.CharField(max_length=20)
    wialon_user = models.ForeignKey(WialonUser,
                                    on_delete=models.PROTECT,
                                    null=True,
                                    blank=True
                                    )
    terminal = models.OneToOneField(Terminals,
                                    on_delete=models.PROTECT,
                                    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WialonObjectActive(models.Model):
    wialon_object = models.OneToOneField(WialonObject,
                                         on_delete=models.CASCADE,
                                         )
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wialon_object)

    class Meta:
        ordering = ['wialon_object']


class WialonServer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserWialonServer(models.Model):
    user = models.OneToOneField(WialonUser,
                                on_delete=models.CASCADE,
                                )
    server = models.ForeignKey(WialonServer,
                               on_delete=models.PROTECT,
                               null=True,
                               blank=True
                               )
