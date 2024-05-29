#!/bin/bash

text_name=$1
workfolder=$2
url=$3
user=$4
password=$5


conda activate llm

python create-knowledge-graph $text_name $workfolder $url $user $password