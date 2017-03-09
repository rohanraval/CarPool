from django import forms
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import scraper

def is_zip_valid(zipCode):
	if not scraper.validateZip(zipCode):
		raise ValidationError("%s is not a valid zip code" % zipCode)

def is_year_valid(year):
	if not scraper.validateYear(year):
		raise ValidationError("%s is not a valid year" % year)

class CarForm(forms.Form):
	start_zip = forms.CharField(label='Start Zip Code', max_length=5, validators=[is_zip_valid], required=True)
	dest_zip = forms.CharField(label='Dest Zip Code', max_length=5, validators=[is_zip_valid], required=True)
	year = forms.CharField(label='Car Year', max_length=4, validators=[is_year_valid], required=True)
	make = forms.ChoiceField(label='Car Make')
	model = forms.ChoiceField(label='Car Model')

	def __init__(self, *args, **kwargs):
		super(CarForm, self).__init__(*args, **kwargs)
		self.fields['make'].widget.attrs['class'] = 'form-control'
		self.fields['make'].widget.attrs['style'] = 'width:150px'
		self.fields['model'].widget.attrs['class'] = 'form-control'
		self.fields['model'].widget.attrs['style'] = 'width:200px'
