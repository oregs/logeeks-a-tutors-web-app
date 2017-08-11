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


def properly_format(student_id):
    return str(student_id).upper()


def calculate_tutor_charge_per_hour(tutor_experience, tutor_rating, tutor_recommendation, tutor_qualification):
    """
    This function accepts a tutor's key info to calculate what amount tutor should earn per hour.

    :param tutor_experience: (int). Years of experience as a tutor
    :param tutor_rating: (float). tutor's cumulative rating/reviews from past all tutor's previous clients
    :param tutor_recommendation: (float). tutor's level of Trust.
    :param tutor_qualification: (float). Academic Qualification of the tutor
    :return: Returns a float, which is the tutor's worth per hour (in Naira) calculated based on the four parameters.
    """
    MAX_AMOUNT = 4000  # Maximum tutor Charge per Hour
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


def student_sign_up(request):
    user = User.objects

    if request.method == 'POST':
        def is_valid_student_id(new_id):
            try:
                user.get(username=new_id)
                return False
            except Exception:
                return True

        student_id = "A1000"
        while not is_valid_student_id(student_id):
            student_id = random.choice(
                ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W', 'X', 'Y', 'Z']) + str(random.randint(1000, 9999))

        username = student_id
        password = request.POST['password']
        first_name = request.POST['first_name'].capitalize()
        middle_name = request.POST['middle_name'].capitalize()
        last_name = request.POST['last_name'].capitalize()
        email = request.POST['email'].lower()
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        photo = request.POST['photo']

        new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        user_id = new_user.id
        new_student = Student(user_id=user_id)
        new_student.user_id = user_id
        new_student.middle_name = middle_name
        new_student.gender = gender
        new_student.phone_number = phone_number
        new_student.address = address
        new_student.photo = photo
        new_student.save()
        # TODO: send_mail() ## Remember to properly implement this to send a mail to the new student to show his/her
        # username
        return redirect('/student/sign_in/')

    context = {}
    return render(request, 'student/student_sign_up.html', context)


# @login_required(login_url='/student/sign_in/', redirect_field_name='next')
def select_tutor(request):
    context = {}
    return render(request, 'student/student_select_tutor.html', context)


# @login_required(login_url='/student/sign_in/', redirect_field_name='next')
def hire_tutor(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        client_lga = request.POST['lga']
        page_num_to_be_displayed = int(request.POST['page_no'])

        valid_tutors_list = []
        # for title in dict_of_subjects_tutors:
        #     if subject == title:
        #
        tutor_model = Tutor
        # tutor_user = None
        all_tutors_list = tutor_model.objects.all()
        for tutor in all_tutors_list:
            if (client_lga == tutor.lga1 or client_lga == tutor.lga2 or client_lga == tutor.lga3) and subject == tutor.subject:
                if tutor.is_visible:
                    valid_tutors_list.append(tutor)
        for tutor in valid_tutors_list:
            # tutor_user = tutor.user
            if (int(timezone.now().year) > int(tutor.user.date_joined.year)) and (int(timezone.now().month) >= int(tutor.user.date_joined.month)):
                years_of_experience = int(timezone.now().year) - int(tutor.user.date_joined.year)
                tutor.experience = years_of_experience
            tutor.save()
            tutor.charge = calculate_tutor_charge_per_hour(tutor.experience, tutor.rating, tutor.recommendation, tutor.qualification)

        num_of_matched_query = len(valid_tutors_list)
        # if the number of tutors per page must be changed, reset highest_num_of_tutors_per_page = the new value.
        # but the valid minimum value for highest_num_of_tutors_per_page should be = 3
        highest_num_of_tutors_per_page = 9
        num_of_tutors_per_row = 3
        number_of_row = [i for i in range(0, (highest_num_of_tutors_per_page+1), num_of_tutors_per_row)]
        limit_dict = {}
        upper_bound = highest_num_of_tutors_per_page
        lower_bound = 0
        page_num = 1
        length_uncovered = len(valid_tutors_list)
        while length_uncovered//highest_num_of_tutors_per_page > 0 or (length_uncovered % highest_num_of_tutors_per_page > 0 and length_uncovered > 0):
            limit_dict[page_num] = valid_tutors_list[lower_bound : upper_bound]
            page_num += 1
            lower_bound = upper_bound
            predicted_upper_bound = upper_bound + highest_num_of_tutors_per_page
            if num_of_matched_query > predicted_upper_bound:
                upper_bound = predicted_upper_bound
            else:
                upper_bound = num_of_matched_query
            length_uncovered -= highest_num_of_tutors_per_page

        available_pages = list(limit_dict.keys())
        if available_pages:
            maximum_page_no = max(available_pages)
            minimum_page_no = min(available_pages)
        else:
            maximum_page_no = 0
            minimum_page_no = 0

        if limit_dict:
            page_to_be_displayed = limit_dict.get(page_num_to_be_displayed, None)
        else:
            page_to_be_displayed = []

        context = {'tutors_to_be_displayed':page_to_be_displayed, 'number_of_rows': number_of_row, 'lga': client_lga,
                   'subject': subject, 'query_match': num_of_matched_query, 'pages': available_pages,
                   'current_page': page_num_to_be_displayed, 'last_page': maximum_page_no,
                   'first_page': minimum_page_no, 'col_sm_value': int(12/num_of_tutors_per_row)}
        return render(request, 'student/student_hire_tutor.html', context)
    return redirect('/student/select_tutor/')


@login_required(login_url='/student/sign_in/', redirect_field_name='next')
def student_dashboard(request):
    user = request.user
    student = user.student
    student_photo = student.photo.url if (student.photo) else None
    context = {'user': user, 'student': student, 'student_photo': student_photo}
    return render(request, 'student/student_dashboard.html', context)


def student_sign_in(request):
    if request.GET:
        next_url=request.GET['next']
    else:
        next_url = '/student/dashboard/'
    error_message = False
    if next_url != '/student/dashboard/':
        additional_message = 'Please sign in continue'
    else:
        additional_message = None
    context = {'error_message': error_message, 'next_url': next_url, 'additional_message': additional_message}
    return render(request, 'student/student_sign_in.html', context)


def authenticating(request):
    error_message = None
    if request.POST:
        student_id = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next']
        student = authenticate(username=properly_format(student_id), password=password)
        if student is not None:
            if student.is_active:
                login(request, student)
                return redirect(next_url)
            else:
                error_message = 'Sorry, but this Account has been deleted!'
        else:
            error_message = 'Invalid student Info'

    if request.GET:
        next_url = request.GET['next']
    else:
        next_url = '/student/dashboard/'
    context = {'error_message': error_message, 'next_url': next_url}
    return render(request, 'student/student_sign_in.html', context)


def student_sign_out(request):
    if request.method == 'POST':
        sign_out = request.POST['sign_out']
        logout_student = True
        logout(request)
    context = {'user_just_logged_out': logout_student}
    return redirect('/')


@login_required(login_url='/student/sign_in/', redirect_field_name='next')
def update_student_password(request):
    password_update_failed = False
    error_message = None
    if request.method == 'POST':
        old_password = request.POST['current_password']
        new_password = request.POST['new_password']
        retyped_new_password = request.POST['retyped_new_password']
        user = request.user
        if new_password != retyped_new_password:
            password_update_failed = True
            error_message = 'The New Password fields does not match!'
        elif not user.check_password(old_password):
            password_update_failed = True
            error_message = 'Current Password typed is incorrect'
        elif (user.first_name.lower() or user.last_name.lower() or user.student.middle_name.lower()) == new_password.lower():
            password_update_failed = True
            error_message = 'Your new password should not be too similar to your other Personal information!'
        elif re.match(r'[0-9]+', new_password):
            password_update_failed = True
            error_message = 'Your password cannot be entirely numeric!'
        elif user.email == new_password:
            password_update_failed = True
            error_message = 'Your new password is too similar to your email address!'
        else:
            user.set_password(new_password)
            user.save()
            logout(request)
            return HttpResponsePermanentRedirect('/student/password_update_successful')
    context = {'password_update_failed': password_update_failed, 'password_update_error_message': error_message}
    return render(request, 'student/student_password_update.html', context)


def password_update_successful(request):
    return render(request, 'student/student_password_update_successful.html')


def student_reset_password(request):
    logout(request)
    template_name = 'student/student_password_reset.html'
    context = {}
    error_occurred = None
    if request.method == 'POST':
        recipient_username = request.POST['recipient_username']
        try:
            user = User.objects.get(username=properly_format(recipient_username))
            uidb64 = recipient_username
            token_generator = default_token_generator.make_token(user)
            context = {'uidb64': uidb64, 'token': token_generator}
            error_occurred = False
            user_email = user.email
            # TODO: Remember to properly uncomment the 2 lines following this.
            # send_email(subject_template_name, email_template_name, context, from_email, to_email,
            #            html_email_template_name=None)

            return redirect('/student/student_password_reset_done')

        except User.DoesNotExist:
            error_occurred = True
    if error_occurred:
        context = {'error_occurred': error_occurred, 'incorrect_username': recipient_username}
    return render(request, template_name, context)


def student_password_reset_done(request):
    logout(request)
    context = {}
    return render(request, 'student/student_password_reset_done.html', context)


def student_password_reset_confirm(request, uidb64=None, token=None,):
    logout(request)
    recipient_username = uidb64
    user = User.objects.get(username=properly_format(recipient_username))
    token_generator = default_token_generator
    if user is not None and token_generator.check_token(user, token):
        link_is_valid = True
        message = 'Successful!'
    else:
        link_is_valid = False
        message = 'Failed! This link is invalid'
    context = {'link_is_valid': link_is_valid, 'message': message, 'student_id': recipient_username}
    return render(request, 'student/student_password_reset_confirm.html', context)


def student_set_new_password(request):
    logout(request)
    error_message = None
    password_update_failed = None
    if request.method == 'POST':
        new_password = request.POST['new_password']
        retyped_new_password = request.POST['retyped_new_password']
        recipient_username = request.POST['student_id']
        properly_formatted_recipient_username = properly_format(recipient_username)
        user = User.objects.get(username=properly_formatted_recipient_username)
        if (new_password != retyped_new_password) and (new_password != ''):
            password_update_failed = True
            error_message = 'The New Password fields does not match!'
        elif (user.first_name.lower() or user.last_name.lower() or user.student.middleName.lower()) == new_password.lower():
            password_update_failed = True
            error_message = 'Your new password should not be too similar to your other Personal information!'
        elif re.match(r'[0-9]+', new_password):
            password_update_failed = True
            error_message = 'Your password cannot be entirely numeric!'
        elif user.email == new_password:
            password_update_failed = True
            error_message = 'Your new password is too similar to your email address!'
        elif new_password == retyped_new_password:
            user.set_password(new_password)
            user.save()
            return HttpResponsePermanentRedirect('/student/student_password_reset_complete')
    context = {'password_update_failed': password_update_failed, 'error_message': error_message,
               'student_id': recipient_username}
    return render(request, 'student/student_set_new_password.html', context)


def student_password_reset_complete(request):
    logout(request)
    context = {}
    return render(request, 'student/student_password_reset_complete.html', context)


@login_required(login_url='/student/sign_in/', redirect_field_name='next')
def student_profile(request):
    user = request.user
    student = user.student
    context = {'user': user, 'student': student}
    return render(request, 'student/student_profile.html', context)


@login_required(login_url='/student/sign_in/', redirect_field_name='next')
def transaction_archive(request):
    context = {}
    return render(request, 'student/transaction_archive.html', context)
