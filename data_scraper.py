# importing dependencies
import requests # request html file of link
from bs4 import BeautifulSoup # html parser to get the data that we need
import numpy as np # vector operations
import pandas as pd # label data
import matplotlib.pyplot as plt # visualize data
from sklearn.linear_model import LinearRegression # process data
import pickle # to use save and reuse model

# NOTE: KIJIJI often changes their html attribute values to avoid parsers, these have
# to be manually scanned and updated for the script to work


# the search result link that will be scraped
# split into 2 as an interger will indicate the page in between
baseSearch = "https://www.kijiji.ca/b-cars-vehicles/canada/equinox/page-"
baseSearch2 = "/k0c27l0?ad=offering&price=3500__"

# get the links of a search page
def get_ads_link(searchLink, numPages):
	# searchLink - the link that will be scraped
	#			   comes in a list of two parts
	# numPages - the number of pages you wish to scrape
	#			 each page has around 20 - 25 unique ads
	
	ads = []

	#loop through pages
	for i in range(1, numPages+1):
	#request the link, then parse it with beautiful soup
		r = requests.get(searchLink[0] + str(i) + searchLink[1])
		soup = BeautifulSoup(r.content)
		listOfDivs = soup.find_all("div")

	#search for divs with correct attributes then save the link
		for div in listOfDivs:
		# data-vip-url is the attribute for the link of the ad that pops up on search
			if div.has_attr("data-vip-url"):

				# retriving the link
				link = div["data-vip-url"]
				# concat strings to result in a proper link in english
				ads.append("https://www.kijiji.ca" + link + "?null&siteLocale=en_CA")

		print("%d of %d" %(i, numPages), end="\r")
	#return unique ads
	return list(set(ads))

# get relevant data from data
def get_ads_data(ads):
	raw_data = []
	errorLog = []
	numAds = len(ads)

	# retrieve html of each ad
	for i, ad in enumerate(ads):
		r = requests.get(ad)
		soup = BeautifulSoup(r.content)

		# getting the price tag of each ad
		try:
			price = soup.find_all("span", {"class": "currentPrice-3369960085"})[0].text
		except:
			try:
				price = soup.find_all("span", {"data-reactid": "39"})[0]["value"]
			except:
				try:
					price = soup.find_all("span", {"data-reactid": "40"})[0]["value"]
				except:
					try:
						price = soup.find_all("span", {"data-reactid": "42"})[0]["value"]
					except:
						errorLog.append(i)
						print("Price Error")

		# retrieve attributes of car
		try:
			# retrieve the label of data and data
			s_data_label = soup.find_all("p", {"class": "attributeLabel-2129198691"}, text=True)
			s_data = soup.find_all("h4", {"class": "attributeValue-4132240161"})
			# check if data matches
			if len(s_data) != len(s_data_label):
				errorLog.append(i)
				print("Data Error")
			else:
				for j in range(len(s_data)):
					s_data[j] = s_data[j].text
					s_data_label[j] = s_data_label[j].text
		except:
			errorLog.append(i)

	    # retrieve title description of the ad
		try:
			title = soup.find_all("h1", {"class": "title-1093844370"})[0].text
		except:
			errorLog.append(i)
			print("Title Error")
		raw_data.append([price, ad, title, [s_data_label, s_data]])
		print("%d of %d" %(i, numAds))

	# remove all ads in the error log
	for index in sorted(errorLog, reverse=True):
		del raw_data[index]

	return raw_data

ads = get_ads_link([baseSearch, baseSearch2], 1)
raw_data = get_ads_data(ads)

with open("raw_data.pkl", "wb") as output_file:
    pickle.dump(raw_data, output_file)