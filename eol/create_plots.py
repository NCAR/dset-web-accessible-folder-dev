#---------------------------------------------------
# This code will take CSV files and plot graphs
# representing EMDAC Metadata completeness scores
#
# Before running, edit the text in 
# input_directory and output_directory statements
# after the import section. All *.csv files should
# be located in the input directory and all the final
# plots will end up in the output_directory
#
#
#---------------------------------------------------
#---------------------------------------------------
#		IMPORT
#---------------------------------------------------

import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import collections
import os

#---------------------------------------------------
#	SET INPUT AND OUTPUT DIRECTORIES
#---------------------------------------------------
currentdir = os.getcwd()
currentdirstring = str(currentdir)
#input_directory = os.fsencode('../LevelsScores/')
input_directory =  './LevelsScores/'
output_directory = '../barcharts/'

#---------------------------------------------------
#	CREATE CORRECT KEYS CORRESPONDING
#	TO METADATE ELEMENTS IN CSV FILES
#---------------------------------------------------

def createTotals():
	totals = collections.OrderedDict.fromkeys(['metadataRecordID', 'ISO assetType', 'metadataContact', 'metadataDate', 'landingPage', 'title', 'publicationDate', 'author', 'publisher', 'abstract', 'resourceSupportContact', 'DataCite resourceType', 'legalConstraints', 'accessConstraints', 'resourceLanguage', '| Tier 2 |', 'otherResponsibleParty/Custodian', 'otherResponsibleParty/Originator', 'otherResponsibleParty/ResourceProvider', 'credit', 'citationDate', 'scienceSupportContact/PI', 'keywords (tags)', 'keywords (GCMD )', 'keywordVocabulary', 'referenceSystem', 'spatialRepresentation', 'spatialResolution', 'ISO topicCategory', 'datasetExtent (Geolocation)', 'datasetExtentDescription', 'temporalCoverage', 'startDate', 'endDate', 'temporalResolution', 'verticalExtent', '| Tier 3 |', 'relatedLinkIdentifier', 'relatedLinkName', 'relatedLinkType', 'relatedlinkDescription', 'alternateIdentifier', 'resourceVersion', 'progress', 'resourceFormat', 'softwareImplementationLanguage', 'additionalInformation', 'distributor', 'distributionFormat', 'assetSize', 'authorIdentifier', '| from Templates |', 'dataIdentification', 'metadataStandardName', 'metadataStandardVersion'], 0) 
	return totals

#--------------------------------------------------
#	LOOP THROUGH FILES IN input_directory
#	TO TOTAL AND PLOT VALUES IN output_directory
#--------------------------------------------------

for filename in os.listdir(input_directory):
# for filename in listdir(input_directory):
	#filename_str = filename.decode("utf-8") 
	#object has already been decoded
	filename_str = filename
	index = filename_str.find('-Scores')
	lab_name = filename_str[0:index] 	#extract lab name from filename
	print('Reading in totals for metadata values from ', lab_name)    
	#with open(input_directory.decode("utf-8") + filename_str, mode='r') as csv_file:
	#removed decode since object is already decoded
	with open(input_directory + filename_str, mode='r') as csv_file:
    		csv_reader = csv.DictReader(csv_file)
    		totals = createTotals()
    		next(csv_reader)
    		for row in csv_reader:
        		del row['archive ident']
        		del row['Total Score']
        		for key in row:
            			row[key] = int(row[key])
            			totals[key] += row[key]
            
	# Create two lists from the totals dictionary to be used for plotting
	labels = list(totals.keys())
	values = list(totals.values())

	print('Creating completeness graph for ', lab_name)
	# Create a figure
	fig = plt.figure(figsize=(20,8))

	# All bars uniform except tier dividers
	colors = ['steelblue' for i in range(len(labels))]
	colors[labels.index('| Tier 2 |')] = 'lightgray'
	colors[labels.index('| Tier 3 |')] = 'lightgray'
	colors[labels.index('| from Templates |')] = 'lightgray'
	
	# Change values at tier dividers
	values[labels.index('| Tier 2 |')] = max(values)
	values[labels.index('| Tier 3 |')] = max(values)
	values[labels.index('| from Templates |')] = max(values)
	
	# Retrieve date information to display on plot
	#today = date.today()

	# Plot metadata type as x-axis and number of datasets containing such as y-axis
	index = np.arange(len(labels))
	scale_index = [3*i for i in index]
	plt.bar(scale_index, values, color=colors, width=2, align='center')
	plt.xlabel('NCAR Dialect', fontsize=15)
	plt.ylabel('Number of metadata files with element', fontsize=15)
	plt.xticks(scale_index, labels, fontsize=11, rotation=45, ha='right')
	plt.title(lab_name.upper()+' Completeness Score', fontsize=20)
	plt.subplots_adjust(bottom=0.4, top=0.9)

	# Set yticks to be integers for values less than 25
	if max(values) == 2:
		yticks = [0,1,2]
		plt.yticks(yticks, yticks, fontsize=11)
	elif max(values) <= 40 :
		yticks = [int(max(values)/4 * i) for i in range(5)]
		plt.yticks(yticks, yticks, fontsize=11)

	# Save figure to output directory as .gif
	fig.savefig(output_directory+lab_name+'.png')
		
	print('Plot saved in the plots directory with the name '+ lab_name+ '.png')

print('Done')
