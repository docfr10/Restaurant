import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from rest_framework.authtoken.admin import User
from django.utils import timezone
from django.db.models import Q
from django.db import models

from datetime import timedelta
from uuid import uuid4


# @todo перевести поля моделей

class Client(models.Model):
    first_name = models.CharField('First name', max_length=50, blank=False)
    last_name = models.CharField('Last name', max_length=50, blank=False)
    middle_name = models.CharField('Middle name', max_length=50, blank=True)
    phone_number = models.CharField('Phone number', max_length=20, blank=False)
    email = models.EmailField('Email', blank=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Pet(models.Model):
    TYPES = (('Cat', 'Cat'),
             ('Dog', 'Dog'))
    name = models.CharField('Name', max_length=50, blank=False)
    type = models.CharField('Type', choices=TYPES, max_length=3, default='Cat')
    weight = models.FloatField('Weight', null=False)
    breed = models.CharField('Breed', max_length=50, blank=False)
    recommendations = models.TextField('Recommendations', max_length=1000, blank=True)

    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Client',
                               related_name='pets')

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'

    def __str__(self):
        return self.name


class Request(models.Model):
    description = models.TextField('Description', max_length=200, blank=False)
    pet = models.ForeignKey('Pet', on_delete=models.SET_NULL, verbose_name='Питомец',
                            related_name='requests', null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    STATUSES = (
        ('Создан', 'Создан'),
        ('Ожидает подписания договора', 'Ожидает подписания договора'),
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('В транспортировке (от владельца)', 'В транспортировке (от владельца)'),
        ('На передержке', 'На передержке'),
        ('В транспортировке (к владельцу)', 'В транспортировке (к владельцу)'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен')
    )
    created_at = models.DateTimeField('Время создания', default=timezone.now)
    duration = models.IntegerField('Длительность, дни')
    status = models.CharField('Статус', choices=STATUSES, max_length=40, default='Создан')
    request = models.OneToOneField('Request', on_delete=models.SET_NULL, verbose_name='Заявка',
                                   related_name='order', null=True)
    workers = models.ManyToManyField('Worker', verbose_name='Работники',
                                     related_name='orders', blank=True)

    def clean(self):
        if self.duration <= 0:
            raise ValidationError('Длительность не может быть менее 1 дня')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)


class Agreement(models.Model):
    description = models.TextField('Description', max_length=200, blank=False)
    price = models.IntegerField('Стоимость, руб.')
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
                                 related_name='agreement', null=True)

    def clean(self):
        if self.price <= 0:
            raise ValidationError('Стоимость не может быть менее 1 руб.')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return str(self.id)


class Worker(models.Model):
    POSITIONS = (
        ('Перевозчик', 'Перевозчик'),
        ('Кипер', 'Кипер')
    )
    first_name = models.CharField('First name', max_length=50, blank=False)
    last_name = models.CharField('Last name', max_length=50, blank=False)
    middle_name = models.CharField('Middle name', max_length=50, blank=True)
    phone_number = models.CharField('Phone number', max_length=20, blank=False)
    email = models.EmailField('Email', blank=True)
    position = models.CharField('Должность', choices=POSITIONS, max_length=40, default='Кипер')

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.position + ' | ' + self.last_name + ' ' + self.first_name


class Car(models.Model):
    POSITIONS = (
        ('Перевозчик', 'Перевозчик'),
        ('Кипер', 'Кипер')
    )
    numbers = models.CharField('Номера', max_length=50)
    mark_n_model = models.CharField('Марка, модель', max_length=50)
    color = models.CharField('Цвет', max_length=50, blank=True)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, verbose_name='Работник',
                               related_name='cars', null=True)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return self.mark_n_model + ' ' + self.numbers


class TransportEvent(models.Model):
    timestamp_start = models.DateTimeField('Время начала', default=timezone.now)
    timestamp_end = models.DateTimeField('Время конца', default=timezone.now)
    description = models.TextField('Описание', max_length=200, blank=False)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
                              related_name='transport_events', null=True)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return str(self.id)
# class Room(models.Model):
#     uid = models.CharField('Уникальный идентификатор', max_length=50, default='none')
#     name = models.CharField('Название', max_length=50)
#     img = models.ImageField('Изображение', upload_to='rooms/images', blank=True)
#     description = models.TextField('Описание', max_length=200, blank=True)
#     recognition_image = models.IntegerField('ID иконки', null=False, blank=True)
#     exposition = models.ForeignKey('Exposition', on_delete=models.CASCADE, verbose_name='Выставка',
#                                    related_name='rooms')
#     connected_rooms = models.ManyToManyField('self', verbose_name='Соединенные комнаты',
#                                              related_name='root_room', blank=True)
#
#     class Meta:
#         verbose_name = 'Комната'
#         verbose_name_plural = 'Комнаты'
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.uid = f'2_{self.id}'
#         super().save(*args, **kwargs)
#
#     def clean(self):
#         if self.recognition_image is not None:
#             if self.recognition_image < ICO_INDEX_MIN or self.recognition_image > ICO_INDEX_MAX:
#                 raise ValidationError(f"ID иконки может быть от {ICO_INDEX_MIN} до {ICO_INDEX_MAX} включительно")
#
#             artifacts = Artifact.objects.filter(
#                 Q(room__exposition=self.exposition),
#                 Q(recognition_image=self.recognition_image)
#             )
#             rooms = Room.objects.filter(
#                 Q(exposition=self.exposition),
#                 Q(recognition_image=self.recognition_image)
#             ).exclude(pk=self.pk)
#             if artifacts.exists():
#                 raise ValidationError(
#                     f"Выбранная иконка уже используется в: {[artifact.name for artifact in artifacts]}")
#             if rooms.exists():
#                 raise ValidationError(f"Выбранная иконка уже используется в: {[room.name for room in rooms]}")
#
#
# class Exposition(models.Model):
#     TYPES = (('По билетам', 'По билетам'),
#              ('Свободный вход', 'Свободный вход'))
#
#     name = models.CharField('Название', max_length=50)
#     description = models.TextField('Описание', max_length=1000, blank=True)
#     type = models.CharField('Тип выставки', choices=TYPES, max_length=64, default='По билетам')
#     ticket_lifetime = models.IntegerField('Время жизни билета (в часах)', default=3)
#     admin = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name='Администратор',
#                                  related_name='exposition', null=True)
#
#     class Meta:
#         verbose_name = 'Выставка'
#         verbose_name_plural = 'Выставки'
#
#     def __str__(self):
#         return self.name
#
#     def clean(self):
#         if self.ticket_lifetime < 1:
#             raise ValidationError(f"Время жизни билета не может быть меньше 1 ч.")
#
#
# class Ticket(models.Model):
#     created_at = models.DateTimeField('Время создания', default=timezone.now)
#     token = models.CharField('Токен', max_length=5000, default='none')
#     exposition = models.ForeignKey('Exposition', on_delete=models.CASCADE, verbose_name='Выставка',
#                                    related_name='tickets', null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Билет'
#         verbose_name_plural = 'Билеты'
#
#     def __str__(self):
#         return f"Билет №{self.id}"
#
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.token = uuid4()
#         super().save(*args, **kwargs)
#
#     @property
#     def is_alive(self):
#         return self.created_at > timezone.now() - timedelta(hours=self.exposition.ticket_lifetime)
#
#     @property
#     def remaining_lifetime(self):
#         duration = timezone.now() - self.created_at  # time that ticket is alive
#         seconds = self.exposition.ticket_lifetime * 3600 - duration.seconds
#         granularity = 1
#         intervals = (
#             ('нед.', 604800),
#             ('дн.', 86400),
#             ('ч.', 3600),
#             ('мин.', 60),
#             ('сек.', 1),
#         )
#         result = []
#         for name, count in intervals:
#             value = seconds // count
#             if value:
#                 seconds -= value * count
#                 if value == 1:
#                     name = name.rstrip('s')
#                 result.append("{} {}".format(value, name))
#         return ', '.join(result[:granularity])
#
#
# class Artifact(models.Model):
#     uid = models.CharField('Уникальный идентификатор', max_length=50, default='none')
#     name = models.CharField('Название', max_length=50)
#     description = models.TextField('Описание', max_length=1000, blank=True)
#     recognition_image = models.IntegerField('ID иконки', null=False, blank=True)
#     room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='Комната',
#                              related_name='artifacts')
#
#     class Meta:
#         verbose_name = 'Экспонат'
#         verbose_name_plural = 'Экспонаты'
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.uid = f'1_{self.id}'
#         super().save(*args, **kwargs)
#
#     def clean(self):
#         if self.recognition_image is not None:
#             if self.recognition_image < ICO_INDEX_MIN or self.recognition_image > ICO_INDEX_MAX:
#                 raise ValidationError(f"ID иконки может быть от {ICO_INDEX_MIN} до {ICO_INDEX_MAX} включительно")
#             artifacts = Artifact.objects.filter(
#                 Q(room__exposition=self.room.exposition),
#                 Q(recognition_image=self.recognition_image)
#             ).exclude(pk=self.pk)
#             rooms = Room.objects.filter(
#                 Q(exposition=self.room.exposition),
#                 Q(recognition_image=self.recognition_image)
#             )
#             if artifacts.exists():
#                 raise ValidationError(
#                     f"Выбранная иконка уже используется в: {[artifact.name for artifact in artifacts]}")
#             if rooms.exists():
#                 raise ValidationError(f"Выбранная иконка уже используется в: {[room.name for room in rooms]}")
#
#
# class MediaLink(models.Model):
#     name = models.CharField('Название', max_length=50)
#     link = models.CharField('Ссылка', max_length=2000)
#     artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE, verbose_name='Экспонат',
#                                  related_name='links')
#
#     class Meta:
#         verbose_name = 'Ссылка'
#         verbose_name_plural = 'Ссылки'
#
#     def __str__(self):
#         return f"Ссылка №{self.id}"
#
#
# class MediaAudio(models.Model):
#     name = models.CharField('Название', max_length=50)
#     audio = models.FileField('Аудиофайл', upload_to='artifacts/audios')
#     artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE, verbose_name='Экспонат',
#                                  related_name='audios')
#
#     class Meta:
#         verbose_name = 'Аудиофайл'
#         verbose_name_plural = 'Аудиофайлы'
#
#     def __str__(self):
#         return f"Аудиофайл №{self.id}"
#
#     def clean(self):
#         approved_file_extensions = ('.mp3', '.ogg', '.wav')
#         if not self.audio.name.lower().endswith(approved_file_extensions):
#             raise ValidationError(
#                 f"Расширение аудиофайла может быть только одим из следующих: {', '.join(approved_file_extensions)}")
#
#         print(self.audio.size, 1048576 * BACKEND_AUDIO_MAX_SIZE)
#         if self.audio.size > 1048576 * BACKEND_AUDIO_MAX_SIZE:
#             raise ValidationError(
#                 f"Размер аудиофайла не может превышать {BACKEND_AUDIO_MAX_SIZE} Мб. Размер текущего файла: {round(self.audio.size / 1048576, 1)} Мб")
#
#
# class MediaImage(models.Model):
#     img = models.ImageField('Изображение', upload_to='artifacts/images')
#     artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE, verbose_name='Экспонат',
#                                  related_name='images')
#
#     class Meta:
#         verbose_name = 'Изображение'
#         verbose_name_plural = 'Изображения'
#
#     def __str__(self):
#         return f"Изображение №{self.id}"
#
#     def clean(self):
#         if self.img.size > 1048576 * BACKEND_IMAGE_MAX_SIZE:
#             raise ValidationError(
#                 f"Размер аудиофайла не может превышать {BACKEND_IMAGE_MAX_SIZE} Мб. Размер текущего файла: {round(self.img.size / 1048576, 1)} Мб")
