#!/bin/bash


for f in "data/inputs"/*; do

	if [[ $f =~ data/inputs/[0-9].* ]]; then
	    ./erkner.py $f
	else
	    :
	fi

done

echo "ERK Name Entity Recognition done"

find data/outputs/ -name 'evaluations_for_*.txt' -exec cp  {} data/erk_evaluations \;

echo "All evaluation files are copied"
