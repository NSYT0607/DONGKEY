from django import forms

from .models import Club
from .models import ClubRule


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = '__all__'

    # def save(self, commit=True):
    #     club = super().save(commit=False)
    #     club.position = True
    #     if commit:
    #         club.save()
    #     return club


class ClubRuleForm(forms.ModelForm):
    class Meta:
        model = ClubRule
        exclude = ('club', )
