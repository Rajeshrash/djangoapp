from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Question,Answer,Comment

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('name', 'dob',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                       'password2','name','dob')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)