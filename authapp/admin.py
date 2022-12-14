from django.contrib import admin
from .models import AbstractUserModel
# Register your models here.


@admin.register(AbstractUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser']
    pass
