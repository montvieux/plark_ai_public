#!/bin/sh
chmod -R 777 ./
find . -type f -name *.py -exec $(pwd)/add_licence.sh '{}' \;