from django import forms

class HelpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    employee_id = forms.IntegerField(label='Employee ID')
    description = forms.CharField(label='Problem Description', widget=forms.Textarea)

class EmployeeSearchForm(forms.Form):
    employee_id = forms.IntegerField(label='Employee ID', required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)

class TrainingSearchForm(forms.Form):
    query = forms.CharField(label='Training ID/Name', max_length=100)
