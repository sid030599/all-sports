from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from facilities.models import Facility


admin.site.register(CustomUser)
