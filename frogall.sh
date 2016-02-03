#!/bin/bash


[ $# -eq 0 ] && { 
	echo "Usage : ./frogall.sh  data/inputs/file/path/" 
	exit
}

for f in $1*; do

	if [[ $f =~ $1[0-9].* ]]; then
	    ./erkfrog.py $f
		:
	else
	    :
	fi

done

echo "All files are Frogged"
