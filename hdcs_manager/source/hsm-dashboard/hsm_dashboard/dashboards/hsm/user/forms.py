
from horizon import forms
from horizon.utils import validators

from django.forms import ValidationError

from hsm_dashboard import api

password_validate_regrex = "^(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[0-9].*)(?=.*[@#$%^&*\.:;~\\\|\[\]\{\}].*).{8,255}$"

class BaseUserForm(forms.SelfHandlingForm):
    def __init__(self, request, *args, **kwargs):
        super(BaseUserForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(forms.Form, self).clean()
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise ValidationError('Passwords do not match.')
        return data


class UpdateUserForm(BaseUserForm):
    id = forms.CharField(label="ID", widget=forms.HiddenInput)
    password = forms.RegexField(label="Password",
            widget=forms.PasswordInput(render_value=False),
            regex=password_validate_regrex,
            required=False,
            error_messages={'invalid':
                    validators.password_validator_msg()})
    confirm_password = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput(render_value=False),
            required=False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateUserForm, self).__init__(request, *args, **kwargs)

        if api.keystone.keystone_can_edit_user() is False:
            for field in ('name', 'password', 'confirm_password'):
                self.fields.pop(field)

    def handle(self, request, data):
        pass