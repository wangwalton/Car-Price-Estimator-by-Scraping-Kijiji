import numpy as np
import pandas as pd
import pickle

with open('raw_data.pkl', 'rb') as handle:
	raw_data = pickle.load(handle)

def extract_structured_data(attributes, r_data):
	structured_data = []
	# Parse through attributes 
	for k in range(len(attributes)):

		# Column of each attribute
		structured_data_attr = []

		# Parse thru raw_data
		for i in range(len(raw_data)):

			len_data_attr = len(raw_data[i][3][0])
			raw_data_contains_attr = False
			# Parse through individual data attributes
			for j in range(len_data_attr):
				if raw_data[i][3][0][j] == attributes[k]:
					structured_data_attr.append(raw_data[i][3][1][j])
					raw_data_contains_attr = True
			# Checks if ad contained the data for this attribute
			if not raw_data_contains_attr:
				structured_data_attr.append(np.nan)
		structured_data.append(structured_data_attr)
	return structured_data

def convertStrToNum(str):
	num = "".join([s for s in str if s.isdigit()])
	if len(num) > 0:
		return int(num)
	else:
		return np.nan

def freqCount(list):
	return {i: list.count(i) for i in list}

def findAttributes(tags, data, setNull=False):
	npData = np.zeros((m,1))

	for i in range(len(data)):
		lineData = data[i]
		containTag = False
		for j in range(len(lineData)):
			for tag in tags:
				value = lineData[j:j+len(tag)].lower()
				if value == tag:
					npData[i,0] = tags[value]
					containTag = True
		if not containTag and setNull:
			npData[i,0] = np.nan
	return npData


filtered_data = extract_structured_data(["Trim", "Year", "Colour", "Drivetrain", "Kilometers"], raw_data)
m = len(raw_data)

# Process price
Y = np.zeros((m, 1))
for i in range(m):
	Y[i,0] = convertStrToNum(raw_data[i][0])

# Process kilometers
kilometers = np.zeros((m,1))
for i in range(len(raw_data)):
	kilometers[i,0] = convertStrToNum(filtered_data[-1][i])

# Process drivetrain
drivetrain_index = {'FWD': 0, 
					'AWD': 1}



drivetrain = np.zeros((m,1))
for i in range(m):
	dt = filtered_data[-2][i]
	if dt == "All-wheel drive (AWD)" or dt == "4 x 4":
		drivetrain[i,0] = 1
	elif dt == 'Front-wheel drive (FWD)' or dt == 'Rear-wheel drive (RWD)':
		drivetrain[i,0] = 0
	else:
		drivetrain[i,0] = np.nan

# Process colours
colour_index = {'Black': 0,
				'Blue': 1,
				'Brown': 2,
				'Burgundy': 3,
				'Gold': 4,
				'Green': 5,
				'Grey': 6,
				'Purple': 7,
				'Red': 8,
				'Silver': 9,
				'Tan': 10,
				'White': 11,
				'NaN': np.NaN,
				'Other': np.NaN}

colours = np.zeros((m,1))
colours_orig = filtered_data[2]
for i in range(m):
	colour = colours_orig[i]
	try:
		colours[i,0] = colour_index[colour]
	except:
		colours[i,0] = np.nan

# Process year into year used
year = np.zeros((m,1))
for i in range(m):
	year[i,0] = 2018 - convertStrToNum(filtered_data[1][i])


#defining indexes
leather_tags = {
    "leather": 1,
    "lthr": 1,
    "leathr": 1,
    "letr":1,
    "leath":1
}
trim_tags = {
    "ls": 0,
    "lt": 1,
    "lt2": 2,
    "2lt": 2,
    "ltz": 3
}
camera_tags = {
    "cam": 1,
    "rear": 1,
    "camera": 1,
    "cmr":1,
    "mera":1,
}
blue_tags = {
    "bluetooth": 1,
    "tooth": 1,
    "toth": 1,
    "blue":1,
    "bth":1,
    "btoth":1
}
cruise_tags = {
    "cc ": 1,
    "cc/": 1,
    "cc,": 1,
    "cc.": 1,
    "cc'": 1,
    "cc;": 1,
    "cruise control": 1,
    "cruise":1,
    "crus": 1,
    "cru": 1
}
remote_tags = {
    "remote control": 1,
    "remote": 1,
    "rcontrol": 1,
    "rmt": 1,
}
sunroof_tags = {
    "sunroof": 1,
    "sun roof": 1,
    "sun_roof": 1,
    "roof": 1,
    "sun": 1,
}
heated_tags = {
    "heated": 1,
    "heated seat": 1,
    "heatedseats": 1,
    "hseats": 1,
    "heat": 1,
}

leatherTest = findAttributes(leather_tags, filtered_data[0])
trimTest = findAttributes(trim_tags, filtered_data[0], setNull=True)
cameraTest = findAttributes(camera_tags, filtered_data[0])
blueTest = findAttributes(blue_tags, filtered_data[0])
remoteTest = findAttributes(remote_tags, filtered_data[0])
sunroofTest = findAttributes(sunroof_tags, filtered_data[0])
heatedTest = findAttributes(heated_tags, filtered_data[0])

clean_data = np.column_stack((kilometers, drivetrain, colours, year, trimTest, leatherTest, cameraTest, blueTest, remoteTest, sunroofTest, heatedTest, Y))

with open("comprised_data.pkl", "wb") as output_file:
    pickle.dump(clean_data, output_file)