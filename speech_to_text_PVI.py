import ui
import speech
import sound
import dialogs
import location
import datetime
import requests
import csv

state_dictionary = {'MA' : 'Massachusetts', 'AL' : 'Alabama', 'AK' : 'Alaska', 'AZ' : 'Arizona', 'AR' : 'Arkansas', 'CA' : 'California', 'CZ' : 'Canal Zone', 'CO' : 'Colorado', 'CT' : 'Connecticut', 'DE' : 'Delaware', 'DC' : 'District of Columbia', 'FL' : 'Florida' , 'GA' : 'Georgia' , 'GU' : 'Guam' , 'HI' : 'Hawaii', 'ID' : 'Idaho' , 'IL' : 'Illionis' , 'IN' : 'Indiana' , 'IA' : 'Lowa' , 'KS' : 'Kansas' , 'KY' : 'Kentucky' , 'LA' : 'Louisiana' , 'ME' : 'Maine' , 'MD' : 'Maryland' , 'MI' : 'Michigan' , 'MN' : 'Minnesota' , 'MS' : 'Mississippi' , 'MO' : 'Missouri' , 'MT' : 'Montana', 'NE' : 'Nebraska' , 'NV' : 'Nevada' , 'NH' : 'New Hampshire', 'NJ' : 'New Jersey', 'NY' : 'New York' , 'NC' : 'North Calorina' , 'ND' : 'North Dakota', 'OH' : 'Ohio' , 'OK' : 'Oklahoma' , 'OR' : 'Orgeon' , 'PA' : 'Pennsylvania' , 'PR' : 'Puerto Rico' , 'RI' : 'Rhode Island' , 'SC' : 'South Carloina' , 'SD' : 'South Dakota' , 'TN' : 'Tennessee' , 'TX' : 'Texas' , 'UT' : 'Utah' , 'VT' : 'Vermont' , 'VI' : 'Virgin Islands' , 'VA' : 'Virginia' , 'WA' : 'Washington' , 'WV' : 'West Virginia', 'WI' : 'Wiscosin' , 'WY' : 'Wyoming'}

def read_csv_file(label1, final_location, label2):
	file_names = []
	d = datetime.datetime.now()
	currYear = d.strftime("%Y")
	currMonth = d.strftime("%m")
	currdDay = d.strftime("%d")
	curent = currYear + currMonth + currdDay
	
	delta = datetime.timedelta(days= 1)
	tempDate = str(d - delta)
	tempYear = tempDate[:4]
	tempMonth = tempDate[5:7]
	tempDay = tempDate[8:10]

	
	url = "https://raw.githubusercontent.com/COVID19PVI/data/master/Model12.4/Model_12.4_" +  tempYear + tempMonth + tempDay + "_results.csv"
	r = requests.get(url)	
	with open('r.txt', 'wb')as file:
		file.write(r.content)
		
	with open('r.txt') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		for row in csv_reader:
			if (line_count == 0):
				line_count +=1
				continue
			else:
				if(row[3] == final_location):
					label2.text = final_location + " County"
					label1.text = str(row[0][0:5])
					speech.say("The current PVI value around " + final_location + "County is " +str(row[0][0:5]), 'en_US')
					break

def speech_to_text(label):
	recorder = sound.Recorder('speech.m4a')
	recorder.record()
	dialogs.alert('Recording...', '','Finish', hide_cancel_button = True)
	recorder.stop()
	result = speech.recognize('speech.m4a')
	#print(result[0][0])
	if "PVI" in result[0][0]:
		best_loc = location.get_location()
		lat = best_loc['latitude']
		lon = best_loc['longitude']
		coordinates = {'latitude': lat, 'longitude': lon}
		results = location.reverse_geocode(coordinates)	
		abr_state = str(results[0]['State'])
		full_state = state_dictionary[abr_state]
		sub_administrative = results[0]['SubAdministrativeArea']
		sub_administrative = sub_administrative.replace(" County" , '')
		final_location = full_state + ', '+sub_administrative
		return final_location
	else:
		return None
		

view = ui.load_view()
my_label = view["label1"]
pvi_label = view["label2"]
view.present("sheet")
final_location = speech_to_text(my_label)
if(final_location):
	read_csv_file(pvi_label, final_location, my_label)

else:
	my_label.text = "Failed Speech recognition"
	pvi_label.text = "Failed Speech recognition"
	speech.say("Failed to recognize speech", 'en_US')
	
