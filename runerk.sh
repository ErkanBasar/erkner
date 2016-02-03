#!/bin/bash


[ $# -eq 0 ] && { 
	echo "Usage : ./runall.sh  data/inputs/frogged-file/path/" 
	echo "        to trigger evaluation mode add '--eval'"
	exit
}

re="data/inputs/frogged/(.+)"
if [[ $1 =~ $re ]]; then  
	export respfol="data/outputs/responses/${BASH_REMATCH[1]}"
fi

for f in $1*; do

	if [[ $f =~ $1[0-9].* ]]; then
	    ./erkner.py $f $2
		:
	else
	    :
	fi

done

echo "ERK Name Entity Recognition done"


for f in $respfol*; do

	if [[ $f =~ $respfol[0-9].* ]]; then
	    ./erknorm.py $f
		:
	else
	    :
	fi

done


echo "Response files are normalized"



if [[ $2 = "--eval" ]]; then
	find data/outputs/ -name 'evaluations_for_*.txt' -exec cp  {} data/erk_evaluations \;
	echo "All evaluation files are copied under 'erk_evaluations'"
else
    :
fi



