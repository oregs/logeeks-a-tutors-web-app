from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from student.models import Student

from django.contrib.auth.models import User
#
# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class StudentInline(admin.StackedInline):
#     model = Student
#     can_delete = False
#     verbose_name_plural = 'students'
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (StudentInline, )
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
