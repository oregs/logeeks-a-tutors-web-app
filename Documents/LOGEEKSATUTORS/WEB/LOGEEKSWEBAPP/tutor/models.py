from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.utils import timezone
from image_cropping import ImageCropField, ImageRatioField


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_list = (('Mathematics', 'Mathematics'), ('English', 'English Language'), ('Biology', 'Biology'),
               ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Further Maths', 'Further Maths'),
               ('Computer Studies', 'Computer Studies'), ('Technical Drawing', 'Technical Drawing'))
    nigeria_lagos_lga = (
        ('apapa', 'apapa'), ('ajah', 'ajah'), ('bariga', 'bariga'), ('ebute-meta', 'ebute-meta'),
        ('eti-osa', 'eti-osa'), ('festac', 'festac'), ('gbagada', 'gbagada'), ('ibeju-lekki', 'ibeju-lekki'),
        ('ifako-ijaye', 'ifako-ijaye'), ('ikeja', 'ikeja'), ('ikorodu', 'ikorodu'),
        ('ikoyi-obalende', 'ikoyi-obalende'),
        ('ilupeju', 'ilupeju'), ('ketu', 'ketu'), ('kosofe', 'kosofe'), ('lagos-island', 'lagos-island'),
        ('lagos-mainland', 'lagos-mainland'), ('magodo', 'magodo'), ('onipanu', 'onipanu'),
        ('oshodi-isolo', 'oshodi-isolo'), ('somolu', 'somolu'), ('surulere', 'surulere'),
        ('victoria-island', 'victoria-island')
    )
    states_in_nigeria = (('lagos', 'lagos'), ('others', 'others'))
    country = models.CharField(max_length=100, default='Nigeria')
    state = models.CharField(max_length=100, choices=states_in_nigeria, default="Lagos, Nigeria")
    lga1 = models.CharField(max_length=100, choices=nigeria_lagos_lga, default='Invalid_lga')
    lga2 = models.CharField(max_length=100, choices=nigeria_lagos_lga, default='Invalid_lga')
    lga3 = models.CharField(max_length=100, choices=nigeria_lagos_lga, default='Invalid_lga')
    # lga_tuple = (lga1, lga2, lga3)
    TUTOR_GENDER = (('Male', 'Male'), ('Female', 'Female'))
    subject = models.CharField(max_length=20, choices=subject_list)
    gender = models.CharField(max_length=6, choices=TUTOR_GENDER, default="Gender")
    middle_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=18)
    address = models.CharField(max_length=200)
    qualification = models.FloatField(default=0)
    recommendation = models.FloatField(default=2.5)
    rating = models.FloatField(default=0.0)
    charge = models.FloatField(default=0.0)
    photo = ImageCropField(upload_to='media/tutor/', editable=True)
    cropping = ImageRatioField('photo', '760x760', allow_fullsize=True, free_crop=True, size_warning=True)
    availability = models.PositiveSmallIntegerField(verbose_name="Tutor's Availability", default=2)
    is_visible = models.BooleanField(default=True)
    experience = models.PositiveSmallIntegerField(default=0)
    # proficiency_level =


    def __str__(self):
        return "Tutor: " + str(self.id)


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
