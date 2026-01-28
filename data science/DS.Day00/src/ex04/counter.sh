#!/bin/sh
INPUT_FILE="../ex03/hh_positions.csv"
OUTPUT_FILE="hh_uniq_positions.csv"

HEADER=$(head -n 1 "$INPUT_FILE")

echo "\"name\",\"count\"" > "$OUTPUT_FILE"
tail -n +2 "$INPUT_FILE" | cut -d'"' -f6 | sort | uniq -c | sort -nr | awk '{
    printf "\"%s\",%d\n", $2, $1
}' >> "$OUTPUT_FILE"

echo "unique saved to $OUTPUT_FILE"