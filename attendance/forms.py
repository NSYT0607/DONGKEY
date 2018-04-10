from django import forms
from .models import Event
from member.models import Member


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('club', )

    def __init__(self, club, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        members = Member.objects.filter(club=club)
        self.fields['absent_member'].choices = [(members[i].pk, members[i].user.username) for i in range(len(members))]


class DateInputForm(forms.Form):
    YEARS = [(None, 'YEAR'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'),]
    MONTHS = [
        (None, "MONTH"), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
        ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
        ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
    ]
    year = forms.ChoiceField(choices=YEARS)
    month = forms.ChoiceField(choices=MONTHS, required=False)