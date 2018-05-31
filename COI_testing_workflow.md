# Test performance of Metaxa2 classifier on Zeale COI sequences

***Use python script to sample 10 percent of reference COI sequences from curated database.***

```
python GetTestTrain.py Curated_DB.fasta
```

\# This creates two files, one containing the testing sequences and the other containing the alternate 90 percent of sequences

***Train the Metaxa2 classifier using the output training sequence file from the previous command.***

\# refer to _COI_curation_workflow.md_ file for details on classifier training

***Use trained classifier to predict the taxonomic composition of the testing sequences***

```
perl /PATH/TO/Metaxa2_2.2/metaxa2 -i Test.fasta -o TEST_REP1_R68 --cpu 28 -g TEST_REP1_DB -R 68
```

***Use python script to compare the predicted taxonomies to the actual taxonomic identities of the testing sequences***

```
python Mtxa2PerformEval.py -dt TrainingDatabase.taxonomies.txt -tt TestingSeqs.taxonomies.txt -pt predicted.taxonomies.txt -op REP1_EVAL
```

***Use trained classifier to predict the taxonomic composition of the testing sequences while forcing family-level classification***

```
perl /PATH/TO/Metaxa2_2.2/metaxa2 -i Test.fasta -o TEST_REP1_ForceFam --cpu 28 -g TEST_REP1_DB --taxlevel 6 
```

***Use python script to align actual taxonomies agains predicted taxonomies in a csv file which includes a column of associated reliability scores***

```
python CurateForLogReg.py predicted.taxonomies.txt actual.taxonomies.txt OutputName.csv
```
