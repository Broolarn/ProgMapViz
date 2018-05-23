import gspread
import matplotlib.pyplot as plt
import numpy as np
import string
from oauth2client.service_account import ServiceAccountCredentials


def setupsheet():
	# read in from sheet
	pythonsheets = sheet.get_all_records()
	Names = sheet.col_values(1);
	Project = sheet.col_values(2);
	Start = sheet.col_values(3);
	End = sheet.col_values(4);

	#convert to arrays 
	Names = np.array(Names)
	Project = np.array(Project)
	Start = np.array(Start)
	End = np.array(End)

	#delete tiles so no problem with comparision etc
	Names = np.delete(Names,0)
	Project = np.delete(Project,0)
	Start = np.delete(Start,0)
	End = np.delete(End,0)

	#right type for conversion
	Start = Start.astype(np.int32)
	End = End.astype(np.int32)
	Project = Project.astype(np.float)

	returnarray = [Names,Project,Start,End]
	return returnarray;


def setupsheetheat():
	# read in from sheet
	pythonsheets = sheet.get_all_records()
	Names = sheet.col_values(7);
	
	Year2015 = sheet.col_values(8);
	Year2016 = sheet.col_values(9);
	Year2017 = sheet.col_values(10);
	Year2018 = sheet.col_values(11);


	
	#delete tiles so no problem with comparision etc
	Names = np.delete(Names,0)
	Year2015 = np.delete(Year2015,0)
	Year2016 = np.delete(Year2016,0)
	Year2017 = np.delete(Year2017,0)
	Year2018 = np.delete(Year2018,0)

	Years = [Year2015[len(Year2015)-1],Year2016[len(Year2016)-1],
		Year2017[len(Year2017)-1],Year2018[len(Year2018)-1]]

	Year2015 = np.delete(Year2015,len(Year2015)-1)
	Year2016 = np.delete(Year2016,len(Year2016)-1)
	Year2017 = np.delete(Year2017,len(Year2017)-1)
	Year2018 = np.delete(Year2018,len(Year2018)-1)
	#convert to arrays 
	Names = np.array(Names)
	Project = np.array([Year2015,Year2016,Year2017,Year2018])
	Project = np.rot90(Project,3)
	Project = np.fliplr(Project)
	



	Project = Project.astype(np.float)

	returnarray = [Names,Project,Years]
	return returnarray;



def Heatplot(HeatNames,Heatmatrix,Years):
	fig, ax = plt.subplots()
	im = ax.imshow(Heatmatrix)


	# We want to show all ticks...
	ax.set_xticks(np.arange(len(Years)))
	ax.set_yticks(np.arange(len(HeatNames)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(Years)
	ax.set_yticklabels(HeatNames)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
	          rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	for i in range(len(HeatNames)):
	    for j in range(len(Years)):
	        text = ax.text(j, i, Heatmatrix[i, j],
	                       ha="center", va="center", color="w")

	ax.set_title("Programing Language used (in Projects/Year)")
	fig.tight_layout()
	plt.show()

def barhplot(Names,End,Start,difference,i):
	if(i==0):
		plt.barh(Names, [1]*(End-Start), left=Start,height=1)
	else:
		plt.barh(range(len(Start)),  difference, left=Start)
		plt.yticks(range(len(Start)), Names)
	plt.show()


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
gclient = gspread.authorize(creds)

sheet = gclient.open("testfile").sheet1

[Names,Project,Start,End] =  setupsheet()

[HeatNames,Heatmatrix,Years] = setupsheetheat()

difference = End - Start


#print stuff barh
# print(type(Start))
# print(Start)
# print(End)
# print(Project)

#print stuff heat
# print(HeatNames)
# print(Heatmatrix)
# print(Years)


# print(Names)
# print(difference)
# if(Names[0]==Names[len(Names)-1]):
# 	print("yes")



Heatplot(HeatNames,Heatmatrix,Years);
barhplot(Names,End,Start,difference,0);
barhplot(Names,End,Start,difference,1);


