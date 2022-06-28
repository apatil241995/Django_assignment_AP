from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'first_name', 'date_of_birth',
                    'is_admin', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User_Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserModelAdmin)