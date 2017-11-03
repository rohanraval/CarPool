from bs4 import BeautifulSoup
import geocoder
import googlemaps
import requests

def validateZip(zipCode):
	return len(zipCode) == 5 and zipCode.isdigit() and geocoder.google(zipCode).country == "US"

def validateYear(year):
	return year.isdigit() and int(year) >= 1985 and int(year) <= 2017

def getCity(zipCode):
	return geocoder.google(zipCode).city + " " + geocoder.google(zipCode).state

def getMakes(year):
	url = "http://www.fueleconomy.gov/ws/rest/vehicle/menu/make?year=" + str(year)
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "xml")

	makes = []
	for make in soup.findAll("text"):
		makes.append(make.text)
	return makes

def getModels(year, make):
	url = "http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=" + str(year) + "&make=" + make
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "xml")

	models = []
	for model in soup.findAll("text"):
		models.append(model.text)
	return models

def getAvgMPG(year, make, model):
	#GET ID OF VEHICLE FROM XML PAGE
	url = "http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=" + year + "&make=" + make + "&model=" + model
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "xml")
	idNum = soup.findAll("value")[0].text

	#GET AVG MPG DATA USING ID
	url = "http://www.fueleconomy.gov/ws/rest/ympg/shared/ympgVehicle/" + str(idNum)
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "xml")

	avgMPG = soup.findAll("avgMpg")[0].text
	return float(avgMPG)

def getDistance(start, dest):
	url = "https://maps.googleapis.com/maps/api/distancematrix/xml?origins=" + str(start) + ",USA&destinations=" + str(dest) + ",USA&mode=driving&&key=AIzaSyBcZgB4kHNoJ8_r5Ehyfm6n-D4Y6VX-_Tg"
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "xml")

	distance = int(soup.distance.value.text) * 0.000621371
	return distance

def gasNeeded(distance, mpg):
	return distance / mpg

def getGasPrice(start):
	stateAbbrev = geocoder.google(start).state
	url = "https://www.gasbuddy.com/USA"
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, "html.parser")
	stateContent = soup.find("a", {"id": stateAbbrev})
	return float(stateContent.find("div", {"class": "text-right"}).text)

def tripCost(gasPrice, gasNeeded):
	return gasPrice * gasNeeded
