# Curate NCBI Fasta Files

**Make sequences continuous by removing next line characters**

awk '/\^\>/ {printf("\\n%s\\n",\$0);next; } { printf("%s",\$0);} END
{printf("\\n");}' \< Arthropod\_COI.fasta \> Arthropod\_COI\_RMNL.fast

**Clean Fasta Headers**

cat Arthropod\_COI\_RMNL.fast | perl -pe ‘s/\^(\>\\d+).\*/\$1/’ \>
Arthropod\_COI\_rmNL.fast

**Use Python script to remove entries with three or more ambiguous base
calls**

python Python\_script\_1.py Arthropod\_COI\_rmNL.fasta

\# This produces the following output file:
Arthropod\_COI\_rmNL\_rmNNN.fasta

**Get list of NCBI Gi Numbers for Sequence Entries**

cat Arthropod\_COI\_rmNL\_rmNNN.fasta | perl -pe ‘s/\^\>(\\d+)/\$1/’ \>
COI.gis

# Get Taxonomies

**Use Perl script from Sickel et al. (2016) (requires NCBI Taxonomy
module)**

perl
/PATH/TO/RDP\_Akenbrand/meta-barcoding-dual-indexing/code/gi2taxonomy.pl
--gis COI.gis --out COI.tax --species COI.species.taxids –genus
COI.genus.taxids

# Run Metaxa2 Database Builder Tool to Extract Zeale Region

perl /PATH/TO/Metaxa2\_2.2/metaxa2\_dbb -o COI\_PRELIM -g COI\_PRELIM -t
COI.tax -i Arthropod\_COI\_rmNL\_rmNNN.fasta -r 1051536662

\# To designate the exact amplicon region of interest, the metabarcoding
primer set can be used to determine 5’ to 3’ region, enabling the user
to trim the sequence and designate it as the representative amplicon
when executing the Metaxa2 Database Builder Tool via the –r flag.

\# We designated a trimmed version of sequence 1051536662, shown below,
as the reference for our work (with the exception of Embioptera and
Strepsiptera, as discussed in the manuscript)

\>1051536662

AATTTGGGCAGGAATAATTGGCTCTTCTTTAAGAATTTTAATTCGAGCAGAATTAGGGAACCCCGGATCTTTAATTGGAGACGACCAAATTTATAATACTATTGTTACAGCTCATGCCTTTATTATAATTTTTTTTATAGTTATACCTATTATAATT

\# After executing this command, the sequences and taxonomies of the
extracted entries can be found in the output directory tree. The
taxonomies are contained in the blast.taxonomy.txt file of the
COI\_PRELIM directory, while the fasta sequences are in the
E.full-length-trimmed-realigned.afa file of the COI\_PRELIM/raw\_data
directory. To remove MAFFT and HMMER processing artifacts, we used a
Perl command to remove ‘-’ characters and the ‘|E’ appended to the Gi
numbers

cat E.full-length-trimmed-realigned.afa | perl –pe ‘s/-//g’ | perl –pe
‘s/\^\>(\\d+)\\|E/\>\$1/’ | awk '{ if (\$0 !\~ /\>/) {print
toupper(\$0)} else {print \$0} }' \> COI\_prelim\_0.fasta

# Curate Taxonomies

**Remove Entries Undefined at Kingdom Rank and Reformat**

cat blast.taxonomy.txt | sed '/k\_\_undef\_\_/d' | perl -pe
's/\^(\\d+).E\\tRoot;/\$1\\t/' | perl -pe 's/\_+\\d+//g' | perl –pe
‘s/\^\>(\\d+)\\.E/\>\$1/’ \> COI\_prelim\_0.tax

**Curate Entries Undefined at Intermediate Taxonomic Ranks**

\# To accomplish this, we deleted undefined rank labels and then treated
each entry like a semicolon separated list, allowing us to search and
replace empty ranks (i.e. ‘;;’)

cat COI\_prelim\_0.tax | perl -pe 's/.\_\_undef//g' \>
COI\_prelim\_1.tax

\# We then searched for empty ranks, determined the appropriate label
based on authoritative taxonomic databases or phylogenetic analyses and
replaced the empty rank with the label as shown in the example below

cat COI\_prelim\_1.tax | perl -pe
's/;(;f\_\_Lepismatidae)/;o\_\_Zygentoma\$1/' \> COI\_prelim\_2.tax

\# the following table shows all the necessary changes

  -------------------------- ------------------------------------------------------------------------
  Original Designation | Curated Designation
  --- | ---
  ;;f\_\_Sphaerotheriidae | ;o\_\_Sphaerotheriida;f\_\_Sphaerotheriidae
  ;;f\_\_Zephroniidae | ;o\_\_Sphaerotheriida;f\_\_Zephroniidae
  ;;f\_\_Lepidotrichidae | ;o\_\_Zygentoma;f\_\_Lepidotrichidae
  ;;f\_\_Lepismatidae | ;o\_\_Zygentoma;f\_\_Lepismatidae
  ;;f\_\_Nicoletiidae | ;o\_\_Zygentoma;f\_\_Nicoletiidae
  ;;o\_\_Pauropoda | ;c\_\_Myriapoda;o\_\_Paurapoda
  ;;g\_\_Pseudocellus | ;f\_\_Riconoididae;g\_\_Pseudocellus
  ;;g\_\_Chanbria | ;f\_\_Eremobatidae;g\_\_Chanbria
  ;;s\_\_Tanypodinae | ;g\_\_Tanypodinae;s\_\_Tanypodinae
  ;;s\_\_Ennominae | ;g\_\_Ennominae;s\_\_Ennominae
  ;;g\_\_Dichelesthiidae | ;f\_\_Dichelesthiidae;g\_\_Dichelesthiidae
  ;;g\_\_Phallocryptus | ;f\_\_Thamnocephalidae;g\_\_Phallocryptus
  ;;;g\_\_Lasionectes | ;o\_\_Nectiopoda;f\_\_Speleonectidae;g\_\_Lasionectes
  ;;;;g\_\_Prionodiaptomus | ;c\_\_Maxillopoda;o\_\_Calanoida;f\_\_Diaptomidae;g\_\_Prionodiaptomus
  ;;o\_\_Symphyla | ;c\_\_Myriapoda;o\_\_Symphyla
  ;;;f\_Peripatidae | ;c\_\_Onychophora;o\_\_Onychophora;f\_\_Peripatidae
  ;;;f\_Peripatopsidae | ;c\_\_Onychophora;o\_\_Onychophora;f\_\_Peripatopsidae
  -------------------------- ------------------------------------------------------------------------

**Curate Leaves of Taxonomic Entries (e.g. sp., cf., nr., etc.)**

\# The following is an example of using Perl substitution to removes
artifacts from taxonomic lineages

cat COI\_prelim\_2.tax | perl -pe 's/s\_\_[A-Za-z]+\\ssp\\.\\s.\*//' \>
COI\_prelim\_3.tax

\# The following non-exhaustive list shows artifacts commonly found in
our sequence data

-   ‘sp.’
-   ‘cf.’
-   ‘gen.’
-   ‘nr.’
-   ‘environmental sample’
-   ‘group’
-   ‘complex’

# Remove Duplicate Sequences

\# For this step, sequence headers must contain the taxonomic lineage of
the entry, which can be done using a Perl script from Sickel et al.
(2016)

perl
\~/PATH/TO/RDP\_Akenbrand/meta-barcoding-dual-indexing/code/tax2rdp\_utax.pl
COI\_prelim\_3.tax COI\_prelim\_0.fasta COI\_prelim\_4

java -Xmx4g -jar
/PATH/TO/RDP\_Akenbrand/rdp\_classifier\_2.11/dist/classifier.jar
rm-dupseq --infile COI\_prelim\_4.rdp.fa --outfile
COI\_prelim\_5.rmDS.fasta --duplicates --min\_seq\_length 50

\# After removing duplicates, create new file of remaining taxonomies
and a separate file for the remaining sequence entries

cat COI\_prelim\_5.rmDS.fasta | perl –pe ‘s/\^\>(\\d+).\*/\>\$1/’ \>
COI\_final.fasta

grep ‘\>’ COI\_prelim\_5.rmDS.fasta | perl –pe ‘s/\^\>//’ \>
COI\_final.tax

\# Check to ensure that the archetypical reference sequence, in this
case Gi 1051536662, is still present in the final dataset

# Train Metaxa2 DNA Sequence Classifier

perl /PATH/TO/Metaxa2\_2.2/metaxa2\_dbb -o COI\_FINAL -g COI\_FINAL -t
COI\_final.tax -i COI\_final.fasta -r 1051536662
