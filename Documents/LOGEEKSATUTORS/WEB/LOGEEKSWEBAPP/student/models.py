from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from image_cropping import ImageCropField, ImageRatioField


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=18)
    address = models.CharField(max_length=90)
    photo = ImageCropField(upload_to='media/tutor/', editable=True)
    cropping = ImageRatioField('photo', '430x430', allow_fullsize=True, free_crop=True, size_warning=True)
    verification = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    num_of_times_blacklisted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Student " + str(self.id)


class Notification(models.Model):
    notification_id = models.CharField(max_length=6, primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    related_transaction = models.CharField(max_length=10)
    message_title = models.CharField(max_length=50)
    message_content = models.CharField(max_length=1000)
    read_status = models.BooleanField(default=False)
    notification_tag = models.CharField(max_length=20)

    def __str__(self):
        return self.notification_id