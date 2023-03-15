from django.db import models


class Refbook(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} {self.code}'

    class Meta:
        ordering = ['name']
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class Version(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    refbook = models.ForeignKey('Refbook',
                                on_delete=models.CASCADE,
                                related_name='versions',
                                verbose_name='Наименование справочника'
                                )
    version = models.CharField(max_length=50, verbose_name='Версия')
    date = models.DateField(verbose_name='Дата начала действия версии')

    def __str__(self):
        return f'{self.refbook}, версия {self.version}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        unique_together = [['refbook', 'version'],
                           ['refbook', 'date']]


class Element(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    version = models.ForeignKey('Version',
                                on_delete=models.CASCADE,
                                related_name='elements',
                                verbose_name='Версия'
                                )
    code = models.CharField(max_length=100, verbose_name='Код элемента')
    value = models.CharField(max_length=300, verbose_name='Значение элемента')

    def __str__(self):
        return f'{self.code}. {self.value}'

    class Meta:
        ordering = ['value', 'code']
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        unique_together = ['version', 'code']
