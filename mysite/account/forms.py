from django import forms
from django.core.exceptions import ValidationError
import re

# Validator to check length of usernames


def validate_username(value):
    if not len(value) >= 5:
        raise ValidationError(
            'Username must be at least 5 characters',
            code='less_than_5'
        )


# Validator to check length and contents of passwords


def validate_password(value):
    if not len(value) >= 5:
        raise ValidationError(
            'Password must be at least 5 characters',
            code='less_than_5'
        )
    if not re.search('[a-z]', value):
        raise ValidationError(
            'Password must contain at least 1 lowercase letter',
            code='no_lowercase'
        )
    if not re.search('[A-Z]', value):
        raise ValidationError(
            'Password must contain at least 1 uppercase letter',
            code='no_uppercase'
        )
    if not re.search('[0-9]', value):
        raise ValidationError(
            'Password must contain at least 1 number',
            code='no_number'
        )


# Sign Up


class SignupForm(forms.Form):
    # Use the custom validator
    username = forms.CharField(
        validators=[validate_username],
        error_messages={'less_than_5': 'Username must be at least 5 characters'})

    password = forms.CharField(
        validators=[validate_password],
        error_messages={
            'less_than_5': 'Username must be at least 5 characters',
            'no_lowercase': 'Password must contain at least 1 lowercase letter',
            'no_uppercase': 'Password must contain at least 1 uppercase letter',
            'no_number': 'Password must contain at least 1 number'
        })
    password_confirm = forms.CharField()

    def clean(self):
        # Auto-cleans the user-entered data before using it
        cleaned_data = super(SignupForm, self).clean()

        # Validation involving multiple fields (check that passwords match)
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data

# Log In


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
