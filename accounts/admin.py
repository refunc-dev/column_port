from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

class CustomUserAdmin(UserAdmin):
    list_display = list(UserAdmin.list_display) + ['custom_field']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('custom_field',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('custom_field',)}),
    )

admin.site.register(User, UserAdmin)