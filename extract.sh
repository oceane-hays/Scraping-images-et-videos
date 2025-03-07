#!/bin/bash

usage() { 
    echo "Hello world"; 
    exit 1; 
}
echo "hello"

synopsis=""

while getopts "r:i:v:p:h" o; do
    case "${o}" in
        r)
            synopsis+="r "${OPTARG}";"
            ;;
        i)
            synopsis+="i "${OPTARG}";"
            usage
            ;;
        v)
            synopsis+=${OPTARG}
            usage
            ;;
        p)
            synopsis+=${OPTARG}
            usage
            ;;
        h)
            synopsis+=${OPTARG}
            usage
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# equivalent de split en python
IFS=';'
read -r -a sinop_list <<< "$synopsis"


# si aucune url n'a ete entree en parametre -> Usage: ./extract.sh <url>
if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    exit 1
fi


# a revoir ...
data=$1
#data=$(curl "$url")
echo "DATA $data"
echo "PATH $data"

for sinop in "${sinop_list[@]}"
do
    key=$(echo "$sinop" | cut -d' ' -f1)
    echo "KEY $key"
    value=$(echo "$sinop" | cut -d' ' -f2-)
    echo "VALUE $value"
    
    if [ "$key" == "r" ]; then
        echo "r"
        cat "$data" | grep -E "$value" 
    fi
done
