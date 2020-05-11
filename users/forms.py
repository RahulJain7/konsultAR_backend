from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


# class UserChangeForm(auth_forms.UserChangeForm):
#     class Meta(auth_forms.UserChangeForm.Meta):
#         model = User


# class UserCreationForm(auth_forms.UserCreationForm):

#     error_message = forauth_formsms.UserCreationForm.error_messages.update(
#         {"duplicate_username": _("This username has already been taken.")}
#     )

#     class Meta(auth_forms.UserCreationForm.Meta):
#         model = User

#     def clean_email(self):
#         email = self.cleaned_data["email"]

#         try:
#             User.objects.get(email=email)
#         except User.DoesNotExist:
#             return email

#         raise ValidationError(self.error_messages["duplicate_username"])


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
