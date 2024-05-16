from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kharin.models import Clients, PhotoSessions, CompletedSessions, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(Clients)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    ...
@admin.register(PhotoSessions)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    ...
@admin.register(CompletedSessions)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    ...

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )


