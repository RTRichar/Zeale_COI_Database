#!/usr/bin/env python

#--$ python GetTestTrain.py input.fasta

import sys
from collections import defaultdict
import random

# populate dictionary with fasta
fasta = defaultdict(list)
with open(sys.argv[1]) as file_one:
    for line in file_one:
        if line.startswith(">"):
            fasta[line.strip(">\n")].append(next(file_one).rstrip())

# set number of seqs to retrieve
count = {'count': 0}
for key in fasta:
        count['count'] += 1
SampleSize = int(count['count'] * 10 / 100)

# subsampe fasta into test dictionary
TestFasta = {}
keys = random.sample(list(fasta), SampleSize)
for i in keys:
        TestFasta[i] = fasta[i]

# subsample fasta into train dictionary
TrainFasta = {}
for a in fasta:
        if a not in keys:
                TrainFasta[a] = fasta[a]

# write dictionaries to file
with open('Test.fasta', 'w') as File:
        for key in TestFasta:
                fkey = '>' + key
                seq = str(TestFasta[key])
                File.write("%s\n%s\n" % (fkey, seq[2:-2]))
with open('Train.fasta', 'w') as File2:
        for key in TrainFasta:
                fkey = '>' + key
                seq = str(TrainFasta[key])
                File2.write("%s\n%s\n" % (fkey, seq[2:-2]))
