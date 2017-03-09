from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import CarForm
import scraper

def year_processing(request):
	year = request.GET.get('year', None)
	data = {
		'is_invalid': not (scraper.validateYear(year)),
		'makes': "None"
	}
	if data['is_invalid'] is False:
		data['makes'] = scraper.getMakes(year)
	return JsonResponse(data)

def get_models(request):
	year = request.GET.get('year', None)
	make = request.GET.get('make', None)
	data = {
		'models': scraper.getModels(year, make)
	}
	return JsonResponse(data)

def is_start_zip_valid(request):
	zipCode = request.GET.get('start_zip', None)
	data = {
		'is_invalid': not (scraper.validateZip(zipCode))
    }
	return JsonResponse(data)

def is_dest_zip_valid(request):
	zipCode = request.GET.get('dest_zip', None)
	data = {
		'is_invalid': not (scraper.validateZip(zipCode))
    }
	return JsonResponse(data)

def is_year_valid(request):
	year = request.GET.get('year', None)
	data = {
		'is_invalid': (year < 1985 or year > 2017)
    }
	return JsonResponse(data)

def getGasInfo(responses):
	gasInfo = {
		'distance': scraper.getDistance(responses['start_zip'], responses['dest_zip']),
		'avgMPG': scraper.getAvgMPG(responses['year'], responses['make'], responses['model']),
	}
	gasInfo['gasNeeded'] = scraper.gasNeeded(gasInfo['distance'], gasInfo['avgMPG'])
	gasInfo['gasPriceStart'] = scraper.getGasPrice(responses['start_zip'])
	gasInfo['tripCost'] = scraper.tripCost(gasInfo['gasPriceStart'], gasInfo['gasNeeded'])
	return gasInfo

def index(request):
	form = CarForm()
	return render(request, 'fuelcalc/index.html', {'form': form })

def results(request):
	responses = {}
	gasInfo = {}
	error = ""
	if request.method == 'POST':
		if scraper.validateZip(request.POST.get("start_zip")) and scraper.validateZip(request.POST.get("dest_zip")) and scraper.validateYear(request.POST.get("year")):
		 	responses['start_zip'] = request.POST.get("start_zip")
			responses['start_city'] = scraper.getCity(responses['start_zip'])
		 	responses['dest_zip'] = request.POST.get("dest_zip")
			responses['dest_city'] = scraper.getCity(responses['dest_zip'])
		 	responses['year'] = request.POST.get("year")
		 	responses['make'] = request.POST.get("make")
		 	responses['model'] = request.POST.get("model")
			gasInfo = getGasInfo(responses)
		else:
			error = "Please go back and correct the listed errors."
	else:
		return
	return render(request, 'fuelcalc/results.html', {'responses':responses, 'gasInfo': gasInfo, 'error': error })
