#!/usr/bin/env python

# sys.argv[1]: input predicted taxonomies, sys.argv[2]: actual taxonomies, sys.argv[3]: outfile name

import sys

TAX = open(sys.argv[2], 'r')
CLASS = open(sys.argv[1], 'r')
OUT = open(sys.argv[3], 'w')

# make dictionary of actual GIs and taxonomies
ACT_TAX = {}
for line in TAX:
	line = line.strip().split('\t')
	GI = line[0]
	LINEAGE = line[1].split(';')
	for i in range(0,8):
		if len(LINEAGE) < 8:
			LINEAGE.append('')
	ACT_TAX[GI] = ','.join(LINEAGE)
# make dictionary of GIs and predicted Taxonomies
PRDCT_TAX = {}
for line in CLASS:
        line = line.strip().split('\t')
        GI = line[0]
        LINEAGE = line[1].split(';')
	for i in range(0,8):
                if len(LINEAGE) < 8:
                        LINEAGE.append('')
	SCORE = line[-1]
	PI = line[-3]
	X = str(','.join(LINEAGE) + ',' + SCORE + ',' + PI)
        PRDCT_TAX[GI] = X

for key in PRDCT_TAX:
	OUT.write(str(key) + ',' + ACT_TAX[key] + PRDCT_TAX[key] + '\n')

OUT.close()
TAX.close()
CLASS.close()
