from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import HaskerUser, Tag, Question, Answer
from .forms import HaskerUserChangeForm, HaskerUserCreationForm


@admin.register(HaskerUser)
class CustomUserAdmin(UserAdmin):
    add_form = HaskerUserCreationForm
    form = HaskerUserCreationForm

    list_display = UserAdmin.list_display + ('avatar', )


admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
