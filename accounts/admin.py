# Django imports
from django.contrib import admin
from django.contrib.auth.models import Group

# Project imports
from accounts.models import User, UserActionLog, TwoFactorCode


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()
    list_per_page = 20
    



# Unregister models
admin.site.unregister(Group)


