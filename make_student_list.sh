#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage:"
    echo "$0 <roster_csv> <out_csv>"
    echo ""
    echo "Description:"
    echo "    Make student-list csv."
    exit
fi

roster_file=$1
out_file=$2


{
while IFS="," read student_id github_id _ _
do 
    if [ "$student_id" != "" ] && [ "$student_id" != "\"identifier\"" ]; then
        echo "$student_id,$github_id" | sed "s/\"//g"
    fi
done < $roster_file
} > $out_file
