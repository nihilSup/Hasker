import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Answer, HaskerUser, Question, Tag


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


class TagsField(forms.CharField):
    def __init__(self, *args, max_tag_len=10, max_tag_count=3, **kwargs):
        self.max_tag_len = max_tag_len
        self.max_tag_count = max_tag_count
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        return re.split('\W+', value)

    def validate(self, value):
        if len(value) > self.max_tag_count:
            raise forms.ValidationError(
                f'More then {self.max_tag_count} tags provided',
                code='invalid',
            )
        for tag_name in value:
            super().validate(tag_name)
            if len(tag_name) > self.max_tag_len:
                raise forms.ValidationError(
                    'Tag %(name)s... is longer then %(length)s',
                    code='invalid',
                    params={
                        'name': tag_name[:self.max_tag_len],
                        'length': self.max_tag_len,
                    },
                )


class QuestionForm(BootsModelForm):
    tags = TagsField()

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')


class AnswerForm(BootsModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
