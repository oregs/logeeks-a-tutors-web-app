import re, random
from django.shortcuts import render, HttpResponseRedirect, HttpResponsePermanentRedirect, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage, send_mass_mail
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from tutor.models import Tutor
from student.models import Student
from transaction.models import Transaction
from django.contrib.auth.models import Permission
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import views
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator


def index(request):
    context = {}
    update_tutors_profile()
    return render(request, 'homepage/index.html', context)


def properly_format(tutor_number):
    """
    This function ensures the tutor_number has the proper format of a typical tutor number. E.g 0004PHY
    :param tutor_number: (str). The current Tutor's number
    :return: a proper format of tutor's number like 0002MTH, instead of 02mth.
    """
    answer = ''
    stringed_tutor_number = str(tutor_number)
    numerical_part_of_tutor_number = stringed_tutor_number[:-3]
    subject_id_of_tutor_number = (stringed_tutor_number[-3:]).upper()
    if len(numerical_part_of_tutor_number) >= 4:
        numerical_part_of_tutor_number = numerical_part_of_tutor_number[-4:]
    num_list = []
    for i in numerical_part_of_tutor_number:
        num_list.append(i)

    while len(num_list) != 4:
        num_list.insert(0, '0')

    for char in num_list:
        answer += char
    return answer + subject_id_of_tutor_number


def calculate_tutor_charge_per_hour(tutor_experience, tutor_rating, tutor_recommendation, tutor_qualification):
    """
    This function accepts a Tutor's key info to calculate what amount Tutor should earn per hour.

    :param tutor_experience: (int). Years of experience as a Tutor
    :param tutor_rating: (float). Tutor's cumulative rating/reviews from past all tutor's previous clients
    :param tutor_recommendation: (float). Tutor's level of Trust.
    :param tutor_qualification: (float). Academic Qualification of the Tutor
    :return: Returns a float, which is the Tutor's worth per hour (in Naira) calculated based on the four parameters.
    """
    MAX_AMOUNT = 4000  # Maximum Tutor Charge per Hour
    recommendation_point = 5  # Of the total point, this is the weight the tutor's recommendation carries.
    qualification_point = 5  # Of the total point, this is the weight the tutor's Academic Qualifications carries.
    rating_point = 5  # Of the total point, this is the weight the tutor's past [cumulative] Rating carries.
    experience_point = 5  # Of the total point, this is the weight the tutor's years of experience carries.
    total_point = 20  # And here is the sum total of the entire points.

    # tutor_experience = 1 if (tutor_experience <= 1) else tutor_experience

    years_of_experience = experience_point if (tutor_experience >= experience_point) else tutor_experience
    num_of_star_rating = rating_point if (tutor_rating >= rating_point) else tutor_rating
    recommendation = tutor_recommendation if (tutor_recommendation < recommendation_point) else recommendation_point
    qualification = tutor_qualification if (tutor_qualification < qualification_point) else qualification_point

    if tutor_rating <= 0:
        total_point -= tutor_rating
        payment_ratio = float(years_of_experience + recommendation + qualification) / total_point
    else:
        payment_ratio = float(
            years_of_experience + num_of_star_rating + recommendation + qualification) / total_point
    return round((payment_ratio * MAX_AMOUNT), 2)


def update_years_of_experience(tutor):
    if (int(timezone.now().year) > int(tutor.user.date_joined.year)) and (
                int(timezone.now().month) >= int(tutor.user.date_joined.month)):
        years_of_experience = int(timezone.now().year) - int(tutor.user.date_joined.year)
        tutor.experience = years_of_experience
        tutor.save()


def update_tutors_profile():
    all_tutors = Tutor.objects.all()
    for tutor in all_tutors:
        update_years_of_experience(tutor)
        valid_rating_value = 0 if (tutor.rating <= 0) else tutor.rating
        valid_recommendation_value = 0 if (tutor.recommendation <= 0) else tutor.recommendation
        valid_qualification_value = 1 if (tutor.qualification <= 0) else tutor.qualification
        tutor.rating = valid_rating_value
        tutor.recommendation = valid_recommendation_value
        tutor.qualification = valid_qualification_value
        tutor.charge = calculate_tutor_charge_per_hour(tutor.experience, valid_rating_value, valid_recommendation_value,
                                                       valid_qualification_value)
        tutor.save()

def query_result(request):
    query_list = str(request.GET['client_query']).split()

    # Some Regex logic to find query match will be coded here

    context = {}
    return render(request, 'homepage/query_result.html', context)