from django.contrib import admin
from employee.models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    list_filter = ("user", 'department')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'sum')
    list_filter = ('member', 'sum')
