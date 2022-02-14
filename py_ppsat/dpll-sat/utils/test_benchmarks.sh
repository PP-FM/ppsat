#!/usr/bin/env bash

if [[ $# -ne 2 ]] && [[ $# -ne 3 ]]; then
    echo "Usage: $0 <benchmark_folder> <solver> [<heuristic>]"
    exit
fi
if [ ! -d $1 ]; then
    echo "$1 is not a directory"
    echo "Usage: $0 <benchmark_folder> <solver> [<heuristic>]"
    exit
fi
solver=$2
heuristic=$3
benchmark_folder=$1
TIMEFORMAT=%R
time_count=0
loops=0
for file in ./$benchmark_folder/*; do
    single_time="$(time (python $solver $file $heuristic) 2>&1 1>/dev/null)"
    time_count=$(echo "$single_time + $time_count" | bc)
    loops=$((loops + 1))
done

echo "$time_count / $loops" | bc -l
