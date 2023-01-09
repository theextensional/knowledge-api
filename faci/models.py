from django.contrib.auth.models import User
from django.db import models


class DatetimeMixin(models.Model):
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_modify = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Member(models.Model):
    class Meta:
        db_table = 'app_faci_member'
        verbose_name = 'Участник встречи'
        verbose_name_plural = 'Участники встречи'


class FaciCanvas(DatetimeMixin, models.Model):
    AIM_TYPE_SOLUTION = 1
    AIM_TYPE_IDEA = 2
    AIM_TYPE_SYNC = 3
    AIM_TYPE_CHOICES = (
        (AIM_TYPE_SOLUTION, 'Принять решение'),
        (AIM_TYPE_IDEA, 'Придумать идею'),
        (AIM_TYPE_SYNC, 'Синхронизироваться между собой'),
    )
    user_creator = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    #  Цель
    aim = models.CharField(verbose_name='Что мы пытаемся достичь?', max_length=255, null=False)
    if_not_reached = models.CharField(verbose_name='Что произойдёт, если цель не будет достигнута?', max_length=255, null=False)
    aim_type = models.IntegerField(verbose_name='Вид встречи', null=False, choices=AIM_TYPE_CHOICES)
    # Подготовка
    dt_meeting = models.DateTimeField(verbose_name='Дата и время', null=True)
    duration = models.IntegerField(verbose_name='Длительность', null=False, default=30)
    place = models.CharField(verbose_name='Место', null=False, default='', max_length=100, blank=True)
    # Ключевые мысли
    key_thoughts = models.TextField(verbose_name='Ключевые мысли', max_length=10000, null=False, default='', blank=True)
    parked_thoughts = models.TextField(verbose_name='Парковка', max_length=10000, null=False, default='', blank=True)

    class Meta:
        db_table = 'app_faci_canvas'
        verbose_name = 'Холст фасилитации'
        verbose_name_plural = 'Холсты фасилитации'
