
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class AnnoucementForm(ModelForm):
    class Meta:
        model = Annoucements
        fields = '__all__'
        exclude = ['host', 'participants']


class EmployeesForm(ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'
        exclude = ['user', 'checkout']


class AssetForm(ModelForm):
    class Meta:
        model = Assests
        fields = '__all__'
        exclude = ['user']


class FaqForm(ModelForm):
    class Meta:
        model = Faq
        fields = '__all__'
        exclude = ['user']


class CheckoutForm(ModelForm):
    class Meta:
        model = Dayend
        fields = '__all__'
        exclude = ['user']
