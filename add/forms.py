from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class numberForm(forms.Form):
	operator = forms.CharField()
	numbers1 = SimpleArrayField(forms.IntegerField())
	rows1 = forms.IntegerField()
	cols1 = forms.IntegerField()
	numbers2 = SimpleArrayField(forms.IntegerField())
	rows2 = forms.IntegerField()
	cols2 = forms.IntegerField()