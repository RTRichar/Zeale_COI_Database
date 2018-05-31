#!/usr/bin/env python

#--$ python Mtxa2PerformEval.py -dt Database.tax -tt TestSeqs.tax -pt Predictions.taxonomy.txt

print '\n'
print '\t\t#######Running Metaxa2 evaluation script#######'
print '\n'
print 'PURPOSE: For a custom built database, this script evaluates the performance of Metaxa2 sequence classification and returns the number of false positives, false negatives, true positives and true negatives. In addition, this script returns genus and species level overclassification information and estimates the accuracy and proportion of sequences assigned for all sequences belonging to eash order in the database.'
print '\n'
print 'USAGE: To use this script, we recomend that users randomly sample 10% of the sequences in their reference database, removing them from the training data. Then use the remaining 90% of reference sequences to train Metaxa2. Upon training Metaxa2, classify the 10% of references which were held out. Then execute this script to obtain a summary of Metaxa2 performance.' 
print '\n'
print 'OUTPUT: This script produces three output files.'
print '\t> FILE ONE: general performance metrics (number of true positive(TP), true negative(TN), false negative(FN) and false positive predictions for each rank from kingdom to species).'
print '\t> FILE TWO: overflassification information (number of genus-level overclassification cases (gOVcases); number of species-level overclassification cases (sOVcases); numbef of genus-level overclassification (gOVs); number of species-level overclassifications (sOVs); number of false positives, true positives, true negatives and false negatives at the family-level for genus-level overclassification cases (Fg_FP, Fg_TP, Fg_FN, Fg_TN); number of false positives, true positives, true negatives and false negatives at the genus-level for species-level overclassification cases (Gs_FP, Gs_TP, Gs_FN, Gs_TN))'
print '\t> FILE THREE: performance by order information (number of family, genus and species-level test sequence cases per order (PbyO_Fcases, PbyO_Gcases, PbyO_Scases); number of family, genus and species-level test sequences assigned (PbyO_Fassigned, PbyO_Gassigned, PbyO_Sassigned); number of family, genus and species-level test sequences incorrectly assigned (PbyO_Ferrored, PbyO_Gerrored, PbyO_Serrored))'
print '\n'

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-dt', '--DbTaxonomies', required = True, help = "Taxonomy file of reference database sequences")
parser.add_argument('-tt', '--TestTaxonomies', required=True, help = "Taxonomy file of test case sequences")
parser.add_argument('-pt', '--PredictedTaxonomies', required=True, help = "Metaxa2 predicted taxonomies of test case sequences")
parser.add_argument('-op', '--OutFilePrefix', required=True, help = "Prefix to be included at the beginning of each output file")
args = parser.parse_args()

# for each input tax file, make a list of the seven ranks to use as a basename for a dictionary of every rank. For each rank, populate the dictionary (GI = TaxName)
DctLst_ttTaxIDs = ['kingdom','phylum','class','order','family','genus','species'] # DctLst = list of dictionaries
for a in range(len(DctLst_ttTaxIDs)):
	DctLst_ttTaxIDs[a] = {}
	with open(args.TestTaxonomies) as ttTaxFile:
		for line in ttTaxFile:
			if len(line.strip().split('\t')[1].split(';')) > a:
				DctLst_ttTaxIDs[a][line.strip().split('\t')[0]] = line.strip().split('\t')[1].split(';')[a] 

DctLst_ptTaxIDs = ['kingdom','phylum','class','order','family','genus','species']
for b in range(len(DctLst_ptTaxIDs)): 
        DctLst_ptTaxIDs[b] = {}
        with open(args.PredictedTaxonomies) as ptTaxFile:
                for line in ptTaxFile:
			if re.search( r'k__[A-Za-z]+;', line) is not None:
	                        if len(line.strip().split('\t')[1].split(';')) > b:
        	                        DctLst_ptTaxIDs[b][line.strip().split('\t')[0]] = line.strip().split('\t')[1].split(';')[b]

DctLst_dbTaxIDs = ['kingdom','phylum','class','order','family','genus','species']
for c in range(len(DctLst_dbTaxIDs)):
        DctLst_dbTaxIDs[c] = {}
        with open(args.DbTaxonomies) as dbTaxFile:
                for line in dbTaxFile:
                        if len(line.strip().split('\t')[1].split(';')) > c: 
                                DctLst_dbTaxIDs[c][line.strip().split('\t')[0]] = line.strip().split('\t')[1].split(';')[c] 

# remove empty string values from dictionaries
for y in [DctLst_ttTaxIDs,DctLst_ptTaxIDs,DctLst_dbTaxIDs]:
	for x in range(len(y)):
		y[x] = dict((k, v) for k, v in y[x].iteritems() if v)

# for each rank, make list of taxa in training data 
LstLst_dbTaxLst = ['kingdom','phylum','class','order','family','genus','species'] # LstLst = list of lists
for d in range(len(LstLst_dbTaxLst)):
	LstLst_dbTaxLst[d] = []
	for key in DctLst_dbTaxIDs[d]:
		if DctLst_dbTaxIDs[d][key] not in LstLst_dbTaxLst[d]:
			LstLst_dbTaxLst[d].append(DctLst_dbTaxIDs[d][key])	

# make dictionary to count FN, FP, TN, TP accross each of the seven ranks
DctLst_Counts = ['kingdom','phylum','class','order','family','genus','species']
for e in range(len(DctLst_Counts)):
        DctLst_Counts[e] = {'FN': 0,'FP': 0,'TP': 0,'TN': 0}

# call negatives
for f in range(len(DctLst_ttTaxIDs)): # for each rank index
	for key in DctLst_ttTaxIDs[f]: # for every key/GI in testing file taxonomies dict
		if key not in DctLst_ptTaxIDs[f]: # if that key/GI doesn't exist in predicted taxonomies dict
			if DctLst_ttTaxIDs[f][key] not in LstLst_dbTaxLst[f]:
				DctLst_Counts[f]['TN'] += 1
			else:
				DctLst_Counts[f]['FN'] += 1

# call positives
for f in range(len(DctLst_ttTaxIDs)): # for each rank index
        for key in DctLst_ttTaxIDs[f]: # for every key/GI in testing file taxonomies dict
                if key in DctLst_ptTaxIDs[f]: # if that key/GI doesn't exist in predicted taxonomies dict
                        if DctLst_ttTaxIDs[f][key] == DctLst_ptTaxIDs[f][key]:
                                DctLst_Counts[f]['TP'] += 1
                        else:
                                DctLst_Counts[f]['FP'] += 1

# write general performance measures to file
ranks = ['kingdom','phylum','class','order','family','genus','species']
OutOneDict = {}
header = ['rank','FN','FP','TN','TP']
for f in range(len(DctLst_Counts)):
	OutOneDict[ranks[f]] = ','.join(str(DctLst_Counts[f][key]) for key in sorted(DctLst_Counts[f]))
with open(str(args.OutFilePrefix + '_GeneralPerformance.csv'), 'w') as OutOne:
	OutOne.write(','.join(header) + '\n')
	for key, value in OutOneDict.iteritems():
		OutOne.write(str(key) + ',' + str(value) + '\n')

# overclass (Fg = Family of genus overclassification case)
OverClassDict = {'gOVcases': 0,'gOVs': 0,'Fg_TN': 0,'Fg_FN': 0,'Fg_TP': 0,'Fg_FP': 0,'sOVcases': 0,'sOVs': 0,'Gs_TN': 0,'Gs_FN': 0,'Gs_TP': 0,'Gs_FP': 0}
for key in DctLst_ttTaxIDs[5]:
	if DctLst_ttTaxIDs[5][key] not in LstLst_dbTaxLst[5]:
		OverClassDict['gOVcases'] += 1
		if key in DctLst_ptTaxIDs[5]:
			OverClassDict['gOVs'] += 1
		if key not in DctLst_ptTaxIDs[4]:
			if DctLst_ttTaxIDs[4][key] not in LstLst_dbTaxLst[4]:
				OverClassDict['Fg_TN'] += 1
			else:
				OverClassDict['Fg_FN'] += 1
		else:
			if key in DctLst_ptTaxIDs[4]:
				if DctLst_ptTaxIDs[4][key] != DctLst_ttTaxIDs[4][key]:
					OverClassDict['Fg_FP'] += 1
				else:
					OverClassDict['Fg_TP'] += 1
for key in DctLst_ttTaxIDs[6]:
        if DctLst_ttTaxIDs[6][key] not in LstLst_dbTaxLst[6]:
                OverClassDict['sOVcases'] += 1
                if key in DctLst_ptTaxIDs[6]:
                        OverClassDict['sOVs'] += 1
		if key not in DctLst_ptTaxIDs[5]:
			if DctLst_ttTaxIDs[5][key] not in LstLst_dbTaxLst[5]:
                                OverClassDict['Gs_TN'] += 1
                        else:
                                OverClassDict['Gs_FN'] += 1
		else:
			if key in DctLst_ptTaxIDs[5]:
	                        if DctLst_ptTaxIDs[5][key] != DctLst_ttTaxIDs[5][key]:
	                                OverClassDict['Gs_FP'] += 1
	                        else:
	                                OverClassDict['Gs_TP'] += 1

with open(str(args.OutFilePrefix + '_OverclassificationResults.csv'), 'w') as OVR:
	for key,value in OverClassDict.iteritems():
		OVR.write(str(key) + ',' + str(value) + '\n')

# Performance by order
EbyO_Fcases = {}
EbyO_Gcases = {}
EbyO_Scases = {}
EbyO_Fassigned = {}
EbyO_Gassigned = {}
EbyO_Sassigned = {}
EbyO_Ferrored = {}
EbyO_Gerrored = {}
EbyO_Serrored = {}
#could add EbyO_fFDR calculation
for order in LstLst_dbTaxLst[3]:
	EbyO_Fcases[order] = 0
	EbyO_Fassigned[order] = 0
	EbyO_Ferrored[order] = 0
        EbyO_Gcases[order] = 0
	EbyO_Gassigned[order] = 0
	EbyO_Gerrored[order] = 0
        EbyO_Scases[order] = 0
	EbyO_Sassigned[order] = 0
	EbyO_Serrored[order] = 0
	for key in DctLst_ttTaxIDs[3]:
		if DctLst_ttTaxIDs[3][key] == order:
			if key in DctLst_ttTaxIDs[4]:
				EbyO_Fcases[order] += 1
			if key in DctLst_ptTaxIDs[4]:
				EbyO_Fassigned[order] += 1
				if key in DctLst_ttTaxIDs[4]:
					if DctLst_ptTaxIDs[4][key] != DctLst_ttTaxIDs[4][key]:
						EbyO_Ferrored[order] += 1
        for key in DctLst_ttTaxIDs[3]:
                if DctLst_ttTaxIDs[3][key] == order:
                        if key in DctLst_ttTaxIDs[5]:
                                EbyO_Gcases[order] += 1
                        if key in DctLst_ptTaxIDs[5]:
                                EbyO_Gassigned[order] += 1
                                if key in DctLst_ttTaxIDs[5]:
                                        if DctLst_ptTaxIDs[5][key] != DctLst_ttTaxIDs[5][key]:
                                                EbyO_Gerrored[order] += 1
        for key in DctLst_ttTaxIDs[3]:
                if DctLst_ttTaxIDs[3][key] == order:
                        if key in DctLst_ttTaxIDs[6]:
                                EbyO_Scases[order] += 1
                        if key in DctLst_ptTaxIDs[6]:
                                EbyO_Sassigned[order] += 1
                                if key in DctLst_ttTaxIDs[6]:
                                        if DctLst_ptTaxIDs[6][key] != DctLst_ttTaxIDs[6][key]:
                                		EbyO_Serrored[order] += 1

# write performance by order to file
EbyOheader = ['order','PbyO_Fcases','PbyO_Fassigned','PbyO_Ferrored','PbyO_Gcases','PbyO_Gassigned','PbyO_Gerrored','PbyO_Scases','PbyO_Sassigned','PbyO_Serrored']
with open(str(args.OutFilePrefix + '_PerformanceByOrder.csv'), 'w') as OutThree:
	OutThree.write(','.join(EbyOheader) + '\n')
	for order in LstLst_dbTaxLst[3]:
		ValList = [EbyO_Fcases[order],EbyO_Fassigned[order],EbyO_Ferrored[order],EbyO_Gcases[order],EbyO_Gassigned[order],EbyO_Gerrored[order],EbyO_Scases[order],EbyO_Sassigned[order],EbyO_Serrored[order]]
		OutThree.write(str(order) + ',' + ','.join(str(v) for v in ValList) +  '\n')
