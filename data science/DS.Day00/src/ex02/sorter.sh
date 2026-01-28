#!/bin/sh
INPUT_FILE="../ex01/hh.csv"
OUTPUT_FILE="hh_sorted.csv"

HEADER=$(head -n 1 "$INPUT_FILE")
echo "$HEADER" > "$OUTPUT_FILE"

tail -n +2 "$INPUT_FILE" | sort -t'"' -k4,4 -k2,2 >> "$OUTPUT_FILE"
echo "sorted to $OUTPUT_FILE"