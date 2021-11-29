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

    def clean(self):
        if self.discount_amount <= 0:
            raise ValidationError('Скидка не может быть меньше 1%')

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
        return 'Заказ №' + str(self.pk)


class Receipt(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    check_closing_date = models.DateTimeField('Дата закрытия чека', default=timezone.now())

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def save(self, *args, **kwargs):
        order = Order.objects.get(pk=self.order.id)
        order.status = 'Оплачен'
        order.save()
        super().save(*args, kwargs)

    def __str__(self):
        return 'Чек №' + str(self.pk)


class Staff(models.Model):
    position = models.ForeignKey('Positions', on_delete=models.CASCADE, verbose_name='Должность',
                                 related_name='staffs')
    last_name = models.CharField('Фамилия', max_length=50, blank=False)
    first_name = models.CharField('Имя', max_length=50, blank=False)
    middle_name = models.CharField('Отчетство', max_length=50, blank=True)
    phone_number = models.CharField('Номер телефона', max_length=20, blank=False)
    work_experience = models.FloatField('Опыт работы(лет)')
    salary = models.IntegerField('Зарплата')

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
    workpiece = models.ForeignKey('Workpieces', on_delete=models.CASCADE, verbose_name='Заготовка',
                                  related_name='workpieces')
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
