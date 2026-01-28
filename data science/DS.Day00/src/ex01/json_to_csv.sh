#!/bin/sh
INPUT_FILE="../ex00/hh.json"
OUTPUT_FILE="hh.csv"

jq -r -f filter.jq "$INPUT_FILE" > "$OUTPUT_FILE"

echo "Saved to $OUTPUT_FILE"