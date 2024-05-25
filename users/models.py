from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=35, verbose_name='город', **NULLABLE)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return (
            f"{self.email}")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


# class Payment(models.Model):
#     PAYMENT_METHOD_CHOICES = [
#         ('cash', 'наличные'),
#         ('card', 'банковский перевод')
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
#     payments_date = models.DateTimeField(auto_now=True, verbose_name='дата оплаты')
#     paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс',
#                                     null=True, blank=True)
#     paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок',
#                                     null=True, blank=True)
#     payment_sum = models.PositiveIntegerField(verbose_name='сумма платежа')
#     payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='card',
#                                       verbose_name='способ оплаты')
#     payment_link = models.URLField(max_length=400, verbose_name='ссылка на оплату', blank=True, null=True)
#     payment_id = models.CharField(max_length=255, verbose_name='идентификатор платежа', blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.user}: {self.payments_date}, {self.payment_sum}, {self.payment_id}' \
#                f'{self.paid_course if self.paid_course else self.paid_lesson}'
#
#     class Meta:
#         verbose_name = 'платеж'
#         verbose_name_plural = 'платежи'
#         ordering = ['-payments_date']  # выбор в обратную сторону (-)