from django.contrib import admin
from django.contrib.auth import admin as auth_admin
# from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from . import models


# from relyhelps.users.forms import UserChangeForm, UserCreationForm

# User = get_user_model()
User = models.User
admin.site.register(User)

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (_('Personal Info'), {'fields': ('first_name', 'last_name', 'mobile', 'email', 'password')}),
#         (_('Permissions'), {'fields': ('is_admin', 'is_staff', 'is_active', 'groups')}),
#         (_('Important dates'), {'fields': ('last_login',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (
#             None,
#             {
#                 'classes': ('wide',),
#                 'fields': ('email', 'password1', 'password2')
#             }
#         ),
#     )
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#     filter_horizontal = ('groups',)
    # readonly_fields = ('last_login', )


# Register your models here.
