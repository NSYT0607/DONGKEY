from django.db import models
from django import forms
from django.utils import timezone


class Accounting(models.Model):
    club = models.OneToOneField(
        'club.Club',
        on_delete=models.CASCADE,
        )

    def account_sum(self):
        account_sum = 0
        for income in self.income_set.all():
            account_sum += income.amount
        for expenditure in self.expenditure_set.all():
            account_sum -= expenditure.amount
        return account_sum


class Classification(models.Model):
    name = models.CharField(max_length=15, verbose_name='분류명')

    def __str__(self):
        return self.name


class Income(models.Model):
    accounting = models.ForeignKey(
        Accounting,
        on_delete=models.CASCADE,
        )

    detail = models.CharField(max_length=500, verbose_name='수입 내역', null=True)
    amount = models.IntegerField(verbose_name='수입 금액', blank=True, null=True)
    classfication = models.ManyToManyField(Classification, blank=True)
    income_at = models.DateField(blank=True, null=True)


class Expenditure(models.Model):
    accounting = models.ForeignKey(
        Accounting,
        on_delete=models.CASCADE,
        )

    detail = models.CharField(max_length=500, verbose_name='지출 내역', null=True)
    amount = models.IntegerField(verbose_name='지출 금액', blank=True, null=True)
    classfication = models.ManyToManyField(Classification, blank=True)
    expd_at = models.DateField(blank=True, null=True)
    receipt = models.ImageField(
        upload_to='expenditure/%Y/%m/%d/',
        blank=True,
        null=True,
        )

    def receipt_url(self):
        if self.receipt:
            receipt_url = self.receipt.url
        else:
            receipt_url = ''
        return receipt_url