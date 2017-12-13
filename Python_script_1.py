#!/usr/bin/env python

import sys
iname = sys.argv[1]

fasta = {}
with open(iname) as file_one:
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

new = {}
for key in fasta:
        s = str(fasta[key])
        if s.find('NNN') == -1:
                new[key] = fasta[key]

ibase = iname.split('.')[0]
output = ibase + '_rmNNN.fasta'
o = open(output, 'w')
for key in new:
        fkey = '>' + key
        seq = str(new[key])
        o.write("%s\n%s\n" % (fkey, seq[2:-2]))
o.close()
