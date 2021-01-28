import django.forms as forms
from django.core.validators import EmailValidator, ValidationError
from .validators import validate_login




class CreateUserForm(forms.Form):
    login = forms.CharField(label='Login', validators=[validate_login])
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.CharField(label='Email', validators=[EmailValidator()])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasło nie jest takie same!')
        else:
            return cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")