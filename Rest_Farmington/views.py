from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from Rest_Farmington.models import Rest_Farmington_Hills
from Rest_Farmington.final_app import *

#from forms import RestForm
# Create your views here.
def index(request):
	#if request.method == 'POST':
	#	form=RestForm(request.POST)
	#	if form.is_valid():
	#		return render(request,'Rest_Farmington/results.html')
	#else:
	#	form = RestForm()
		
	return render(request,'Rest_Farmington/index.html')
	
def city(request):
	return render(request,'Rest_Farmington/city.html')
	
def about(request):
	return render(request,'Rest_Farmington/about.html')
	
def contactus(request):
	return render(request,'Rest_Farmington/contactus.html')

	
def results(request):
	return render(request,'Rest_Farmington/results.html')
	
def maps(request):
	if 'restaurant' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		restaurant=request.GET['restaurant']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
		message = 'You entered restaurant: %r and city : %r ' % (restaurant, zipcode)
		return render(request,'Rest_Farmington/maps.html',{'restaurant':restaurant,'zipcode':zipcode,'miles':miles})
	#return render(request,'Rest_Farmington/maps.html')
	else:
		return HttpResponse('You submitted an empty form.')

from Rest_Farmington.forms import RestForm
 
	
#def maps(request):
#    if request.method == 'POST':
#		form = RestForm(request.POST)
#		if form.is_valid():
#			restaurant = form.cleaned_data['restaurant']
#			zipcode = form.cleaned_data['zipcode']
#			miles = form.cleaned_data['miles']
#			post = objects.create(restaurant=restaurant, zipcode=zipcode, miles=miles)
#			return render(request,'Rest_Farmington/index.html')
		
#		else:
#			form = RestForm()
#		return render(request, 'Rest_Farmington/maps.html')
