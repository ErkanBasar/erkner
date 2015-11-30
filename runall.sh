#!/bin/bash


for f in "data/inputs"/*; do

	if [[ $f =~ data/inputs/[0-9].* ]]; then
	    ./erkner.py $f
	else
	    :
	fi

done

find data/outputs/ -name 'evaluations_for_*.txt' -exec cp  {} data/erkevaluations \;
