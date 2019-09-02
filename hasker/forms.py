from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from .models import HaskerUser, Question, Tag, Answer


class HaskerUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('avatar', )


class HaskerUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'


class BootsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label or ''
            })


class UserForm(BootsModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_re = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_re', 'email', 'avatar')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True


class QuestionForm(BootsModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['tags'] = [
                tag.pk for tag in kwargs['instance'].tag_set.all()]
        super().__init__(*args, **kwargs)


class AnswerForm(BootsModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
