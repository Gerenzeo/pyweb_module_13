from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput

class RegisterForm(UserCreationForm):
    username = CharField(max_length=100, required=True, widget=TextInput())
    first_name = CharField(max_length=150, widget=TextInput())
    last_name = CharField(max_length=150, widget=TextInput())
    email = EmailField(max_length=150, required=True, widget=EmailInput())
    password1 = CharField(max_length=20, required=True, min_length=5, widget=PasswordInput())
    password2 = CharField(max_length=20, required=True, min_length=5, widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = CharField(max_length=100, required=True, widget=TextInput())
    password = CharField(max_length=20, required=True, min_length=5, widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
