from django import forms
from .models import Income, Expenditure


class IncomeForm(forms.ModelForm):
    income_at = forms.DateField()

    class Meta:
        model = Income
        exclude = ('accounting', )
    prefix = 'income'


class ExpenditureForm(forms.ModelForm):
    expd_at = forms.DateField()

    class Meta:
        model = Expenditure
        exclude = ('accounting', )
    prefix = 'expd'


class DateInputForm(forms.Form):
    YEARS = [(None, 'YEAR'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'),]
    MONTHS = [
        (None, "MONTH"), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
        ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
        ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
    ]
    year = forms.ChoiceField(choices=YEARS)
    month = forms.ChoiceField(choices=MONTHS, required=False)

