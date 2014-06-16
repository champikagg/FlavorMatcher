from django import forms
from Rest_Farmington.models import Rest_Farmington_Hills

class RestForm(forms.Form):
	restaurant = forms.CharField(max_length=50)
	zipcode = forms.CharField(max_length=50)
	miles=forms.CharField(max_length=10)