from django import forms
from django.core.exceptions import ValidationError

# Validator to check length of usernames


def validate_username(value):
    if not len(value) >= 5:
        raise ValidationError(
            'Username must be at least 5 characters',
            code='less_than_5'
        )

# Sign Up


class SignupForm(forms.Form):
    # Use the custom validator
    username = forms.CharField(
        validators=[validate_username],
        error_messages={'less_than_5': 'Username must be at least 5 characters.'})

    password = forms.CharField()
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
