#!/bin/bash

for f in $1*; do

	if [[ $f =~ $1[0-9].* ]]; then
	    ./erkner.py $f $2
		#write "./runall.sh "folder/path" --eval" to trigger evaluation in erkner 
		:
	else
	    :
	fi

done

echo "ERK Name Entity Recognition done"

find data/outputs/ -name 'evaluations_for_*.txt' -exec cp  {} data/erk_evaluations \;

echo "All evaluation files are copied"
