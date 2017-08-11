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
    num_of_star_rating = rating_point if (tutor_rating>=rating_point) else tutor_rating
    recommendation = tutor_recommendation if (tutor_recommendation < recommendation_point) else recommendation_point
    qualification = tutor_qualification if (tutor_qualification < qualification_point) else qualification_point

    if tutor_rating <= 0:
        total_point -= tutor_rating
        payment_ratio = float(years_of_experience + recommendation + qualification) / total_point
    else:
        payment_ratio = float(years_of_experience + num_of_star_rating + recommendation + qualification) / total_point
    return round((payment_ratio * MAX_AMOUNT), 2)


# @login_required(login_url='/student/sign_in/', redirect_field_name='next')
def initialize_transaction(request):
    if request.method=='POST':
        hired_tutor_number = request.POST['hired_tutor_number']
        hired_tutor_user = User.objects.get(username=hired_tutor_number)
        hired_tutor = hired_tutor_user.tutor
        hired_tutor.charge = calculate_tutor_charge_per_hour(hired_tutor.experience, hired_tutor.rating,
                                                             hired_tutor.recommendation,hired_tutor.qualification)
        hired_tutor.save()
        context = {'hired_tutor': hired_tutor, 'hired_tutor_number': hired_tutor_number, 'hired_tutor_user': hired_tutor_user}
        return render(request, 'transaction/initialize_transaction.html', context)
    return redirect('/student/select_tutor/')


@login_required(login_url='/student/sign_in/', redirect_field_name='next')
def confirm_transaction(request):
    if request.method=='POST':
        hired_tutor_number = request.POST['hired_tutor_number']
        num_of_days_per_week = request.POST['num_of_days_per_week']
        num_of_hours_per_day = request.POST['num_of_hours_per_day']
        tutor_user = User.objects.get(username=hired_tutor_number)
        tutor = tutor_user.tutor
        tutor.charge = calculate_tutor_charge_per_hour(tutor.experience, tutor.rating, tutor.recommendation,
                                                                tutor.qualification)
        tutor.save()
        transport_fare_per_day = 500.0
        num_of_weeks_in_a_month = 4
        total_tuition = (float(num_of_days_per_week) * float(num_of_hours_per_day) * num_of_weeks_in_a_month) * \
                        tutor.charge
        total_transport_fare = transport_fare_per_day * float(num_of_days_per_week) * float(num_of_weeks_in_a_month)
        total_amount_due = total_tuition + total_transport_fare
        context = {'tutor': tutor, 'tutor_charge_per_hour': tutor.charge, 'tutor_user': tutor_user,
                   'total_tuition': total_tuition, 'transport_fare_per_day': transport_fare_per_day,
                   'total_transport_fare': total_transport_fare, 'total_amount_due': total_amount_due}
        tutor.availability = (tutor.availability-1) if (tutor.availability > 0) else 0
        tutor.save()
        return render(request, 'transaction/confirm_transaction.html', context)
    return redirect('/student/select_tutor/')

