from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .domain import BootsModelForm


class HaskerUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('avatar', )


class HaskerUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'


class UserForm(BootsModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_re = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_re', 'email', 'avatar')

    def clean(self):
        cleaned_data = super().clean()
        if(cleaned_data['password'] != cleaned_data['password_re']):
            self.add_error('password', 'Passwords do not match')
            self.add_error('password_re', 'Passwords do not match')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
