from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=5, primary_key=True)
    date_initialized = models.DateField(verbose_name='Initialization Date', default=timezone.now)
    student_id = models.CharField(max_length=10)
    tutor_number = models.CharField(max_length=10)
    total_amount_due = models.FloatField()
    payment_status = models.BooleanField(default=False)
    num_of_days_per_week = models.IntegerField()
    hours_per_day = models.IntegerField()
    validated = models.BooleanField(default=False)
    report_tutor = models.BooleanField(default=False)
    blacklist_student = models.BooleanField(default=False)
    tutor_notified = models.BooleanField(default=False)
    student_notified = models.BooleanField(default=False)
    tutor_bank_account_name = models.CharField(max_length=50, default='Guaranty Trust Bank (GTB)')
    tutor_bank_account_number = models.CharField(max_length=10, verbose_name='Tutor NUBAN')
    tutor_payment = models.FloatField()

    def __str__(self):
        return str(self.transaction_id) + '- between Student ' + str(self.student_id) + ' and Tutor ' + str(self.tutor_number)