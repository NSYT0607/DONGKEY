from django import forms
from .models import AdminResume, ApplicantResume, Question, ShortAnswer, LongAnswer


class AdminResumeForm(forms.ModelForm):
    class Meta:
        model = AdminResume
        exclude = ('club', )


class ApplicantResumeForm(forms.ModelForm):
    class Meta:
        model = ApplicantResume
        fields = ('image', )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('admin_resume',)
    prefix = 'question'


class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = ShortAnswer
        fields = ('content',)
    prefix = 'short_answer'


class LongAnswerForm(forms.ModelForm):
    class Meta:
        model = LongAnswer
        fields = ('content',)
    prefix = 'long_answer'


class AcceptForm(forms.ModelForm):
    class Meta:
        model = ApplicantResume
        fields = ('is_accepted',)
