import django
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


class RegularCustomer(models.Model):
    STATUSES = (('Бронзовый', 'Бронзовый'),
                ('Серебрянный', 'Серебрянный'),
                ('Золотой', 'Золотой'),
                ('Платиновый', 'Платиновый'))
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    first_name = models.CharField('Имя', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
    discount_amount = models.IntegerField('Размер скидки')
    client_status = models.CharField('Статус клиента', choices=STATUSES, max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if 1 <= self.discount_amount <= 5:
            self.client_status = 'Бронзовый'
        elif 6 <= self.discount_amount <= 10:
            self.client_status = 'Серебрянный'
        elif 11 <= self.discount_amount <= 15:
            self.client_status = 'Золотой'
        else:
            self.client_status = 'Платиновый'
        super().save(*args, kwargs)

    class Meta:
        verbose_name = 'Постоянный клиент'
        verbose_name_plural = 'Постоянные клиенты'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Order(models.Model):
    STATUSES = (('Создан', 'Создан'),
                ('Отменен', 'Отменен'),
                ('Отдан на кухню', 'Отдан на кухню'),
                ('Готовится', 'Готовится'),
                ('На подаче', 'На подаче'),
                ('Ожидает оплаты', 'Ожидает оплаты'),
                ('Оплачен', 'Оплачен'))
    status = models.CharField('Статус заказа', choices=STATUSES, max_length=50, default='Создан', blank=True)
    employer = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='Сотрудник',
                                 related_name='orders')  # Добавить чтобы можно было выбирать только из официантов
    composition = models.ManyToManyField('Dishes', verbose_name='Состав заказа',
                                         related_name='orders')
    cost_of_the_order = models.IntegerField('Стоимость заказа', blank=False)
    customer = models.ForeignKey('RegularCustomer', on_delete=models.CASCADE, verbose_name='Карта постоянного клиента',
                                 related_name='orders', blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return '№' + str(self.pk)


class Staff(models.Model):
    position = models.ForeignKey('Positions', on_delete=models.CASCADE, verbose_name='Должность',
                                 related_name='staffs')
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    first_name = models.CharField('Имя', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
    work_experience = models.FloatField('Опыт работы(лет)')
    salary = models.IntegerField('Зарплата')  # Здесь можно сделать расчет з/п исходя из опыта работы

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Positions(models.Model):
    position = models.CharField('Должность', max_length=50)
    responsibilities = models.TextField('Обязанности', max_length=1000)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.position


class Dishes(models.Model):
    name = models.CharField('Название', max_length=50)
    price = models.FloatField('Цена')
    workpiece = models.OneToOneField('Workpieces', on_delete=models.CASCADE, verbose_name='Заготовка')
    equipment = models.TextField('Оборудрвание', max_length=500)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Workpieces(models.Model):
    name = models.CharField('Название', max_length=50)
    ingredients = models.TextField('Ингредиенты', max_length=500)
    batch = models.ManyToManyField('Batch', verbose_name='Партия',
                                   related_name='workpieces')
    date_of_creation = models.DateTimeField('Дата создания')
    expiration_date = models.DateTimeField('Дата истечения срока годности')

    class Meta:
        verbose_name = 'Заготовка'
        verbose_name_plural = 'Заготовки'

    def __str__(self):
        return self.name + ' от ' + str(self.date_of_creation)


class Batch(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, verbose_name='Поставщик', related_name='batchs')
    ingredients = models.TextField('Состав поставки', max_length=500)
    number_of_positions = models.IntegerField(
        'Количество позиций', blank=True)  # Сделать чтобы заполнядлось сам на основании Ингедитентов
    delivery_date = models.DateTimeField('Дата доставки', default=timezone.now)

    class Meta:
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'

    def save(self, *args, **kwargs):
        self.number_of_positions = len(self.ingredients.split(','))
        super().save(*args, kwargs)

    def __str__(self):
        return '№' + str(self.pk)


class Supplier(models.Model):
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    first_name = models.CharField('Имя', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.last_name + ' ' + self.first_name

# class Client(models.Model):
#     first_name = models.CharField('Имя', max_length=50, blank=False)
#     last_name = models.CharField('Фамилия', max_length=50, blank=False)
#     middle_name = models.CharField('Отчетство', max_length=50, blank=True)
#     phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
#     email = models.EmailField('Email', blank=True)
#
#     class Meta:
#         verbose_name = 'Клиент'
#         verbose_name_plural = 'Клиенты'
#
#     def __str__(self):
#         return self.last_name + ' ' + self.first_name
#
#
# class Pet(models.Model):
#     TYPES = (('Кошка', 'Кошка'),
#              ('Собака', 'Собака'))
#     name = models.CharField('Кличка', max_length=50, blank=False)
#     type = models.CharField('Вид', choices=TYPES, max_length=30, default='Кошка')
#     weight = models.FloatField('Вес', null=False)
#     breed = models.CharField('Порода', max_length=50, blank=False)
#     recommendations = models.TextField('Рекомендации', max_length=1000, blank=True)
#
#     client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент',
#                                related_name='pets')
#
#     class Meta:
#         verbose_name = 'Питомец'
#         verbose_name_plural = 'Питомцы'
#
#     def __str__(self):
#         return self.name
#
#
# class Request(models.Model):
#     description = models.TextField('Описание', max_length=200, blank=False)
#     pet = models.ForeignKey('Pet', on_delete=models.SET_NULL, verbose_name='Питомец',
#                             related_name='requests', null=True)
#
#     class Meta:
#         verbose_name = 'Заявка'
#         verbose_name_plural = 'Заявки'
#
#     def __str__(self):
#         return 'Заявка №' + str(self.id)
#
#
# class Order(models.Model):
#     STATUSES = (
#         ('Создан', 'Создан'),
#         ('Ожидает подписания договора', 'Ожидает подписания договора'),
#         ('Ожидает оплаты', 'Ожидает оплаты'),
#         ('В транспортировке (от владельца)', 'В транспортировке (от владельца)'),
#         ('На передержке', 'На передержке'),
#         ('В транспортировке (к владельцу)', 'В транспортировке (к владельцу)'),
#         ('Завершен', 'Завершен'),
#         ('Отменен', 'Отменен')
#     )
#     created_at = models.DateTimeField('Время создания', default=timezone.now)
#     duration = models.IntegerField('Длительность, дни')
#     status = models.CharField('Статус', choices=STATUSES, max_length=40, default='Создан')
#     request = models.OneToOneField('Request', on_delete=models.SET_NULL, verbose_name='Заявка',
#                                    related_name='order', null=True)
#     workers = models.ManyToManyField('Worker', verbose_name='Работники',
#                                      related_name='orders', blank=True)
#
#     def clean(self):
#         if self.duration <= 0:
#             raise ValidationError('Длительность не может быть менее 1 дня')
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     def __str__(self):
#         return 'Заказ №' + str(self.id)
#
#
# class Agreement(models.Model):
#     description = models.TextField('Описание', max_length=200, blank=False)
#     price = models.IntegerField('Стоимость, руб.')
#     order = models.OneToOneField('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                                  related_name='agreement', null=True)
#
#     def clean(self):
#         if self.price <= 0:
#             raise ValidationError('Стоимость не может быть менее 1 руб.')
#
#     class Meta:
#         verbose_name = 'Договор'
#         verbose_name_plural = 'Договоры'
#
#     def __str__(self):
#         return 'Договор №' + str(self.id)
#
#
# class Worker(models.Model):
#     POSITIONS = (
#         ('Перевозчик', 'Перевозчик'),
#         ('Кипер', 'Кипер')
#     )
#     first_name = models.CharField('Имя', max_length=50, blank=False)
#     last_name = models.CharField('Фамилия', max_length=50, blank=False)
#     middle_name = models.CharField('Отчетство', max_length=50, blank=True)
#     phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
#     email = models.EmailField('Email', blank=True)
#     position = models.CharField('Должность', choices=POSITIONS, max_length=40, default='Кипер')
#
#     class Meta:
#         verbose_name = 'Работник'
#         verbose_name_plural = 'Работники'
#
#     def __str__(self):
#         return self.position + ' | ' + self.last_name + ' ' + self.first_name
#
#
# class Car(models.Model):
#     POSITIONS = (
#         ('Перевозчик', 'Перевозчик'),
#         ('Кипер', 'Кипер')
#     )
#     numbers = models.CharField('Номера', max_length=50)
#     mark_n_model = models.CharField('Марка, модель', max_length=50)
#     color = models.CharField('Цвет', max_length=50, blank=True)
#     worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, verbose_name='Работник',
#                                related_name='cars', null=True)
#
#     class Meta:
#         verbose_name = 'Машина'
#         verbose_name_plural = 'Машины'
#
#     def __str__(self):
#         return self.mark_n_model + ' ' + self.numbers
#
#
# class TransportEvent(models.Model):
#     timestamp_start = models.DateTimeField('Время начала', default=timezone.now)
#     timestamp_end = models.DateTimeField('Время конца', default=timezone.now)
#     description = models.TextField('Описание', max_length=200, blank=False)
#     order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                               related_name='transport_events', null=True)
#
#     class Meta:
#         verbose_name = 'Событие перевозки'
#         verbose_name_plural = 'События перевозки'
#
#     def __str__(self):
#         return 'Перевозка №' + str(self.id)
#
#
# class Report(models.Model):
#     created_at = models.DateTimeField('Время создания', default=timezone.now)
#     description = models.TextField('Описание', max_length=200, blank=False)
#     order = models.ForeignKey('Order', on_delete=models.SET_NULL, verbose_name='Заказ',
#                               related_name='reports', null=True)
#     video = models.FileField('Видеофайл', upload_to='report_videos')
#     image = models.ImageField('Изображение', upload_to='report_images')
#
#     def clean(self):
#         approved_video_extensions = ('.mp4', '.ogv', '.webm', 'webvtt')
#         if not self.video.name.lower().endswith(approved_video_extensions):
#             raise ValidationError(
#                 f"Расширение видеофайла может быть только одим из следующих: {', '.join(approved_video_extensions)}")
#
#     class Meta:
#         verbose_name = 'Отчет'
#         verbose_name_plural = 'Отчеты'
#
#     def __str__(self):
#         return 'Отчет №' + str(self.id)
