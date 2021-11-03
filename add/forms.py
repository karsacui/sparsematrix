from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class numberForm(forms.Form):
	numbers = SimpleArrayField(forms.IntegerField())
	rows = forms.IntegerField()
	cols = forms.IntegerField()