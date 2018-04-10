from django import forms
from django.contrib.auth.models import User

from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class MemberClub(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
