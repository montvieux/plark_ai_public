#!/bin/sh
chmod -R 777 ./
for i in *.py
do
	echo "adding licences to $1" 
	$1 
	cat $(pwd)/licence.txt $1 > $1.new && mv $1.new $1 
done