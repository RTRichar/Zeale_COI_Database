#!/usr/bin/env python

### script reads input fasta (sys.argv[1]) into dictionary then writes cropped fasta sequences into outfile (sys.argv[3]) based on length specified by sys.argv[2]
### example: python crop_sequences.py input.fasta 80 output.fasta

import sys

crop_length = int(sys.argv[2]) + 1

fasta = {}
with open(sys.argv[1]) as file_one:
    for line in file_one:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            active_sequence_name = line[1:]
            if active_sequence_name not in fasta:
                fasta[active_sequence_name] = []
            continue
        sequence = line
        fasta[active_sequence_name].append(sequence)

outfile = open(sys.argv[3], 'w')
for key, value in fasta.items():
        outfile.write( '>' + str(key) + '\n' + str(value).strip('[ | ]')[1:crop_length] + '\n' )

file_one.close()
outfile.close()
