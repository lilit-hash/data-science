#!/bin/sh
OUTPUT_FILE="hh_concatenated.csv"
rm -f "$OUTPUT_FILE"

FILES=$(ls *.csv | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}\.csv$')

if [ -z "$FILES" ]; then
    echo "no files"
    exit 1
fi

HEADER=$(head -n 1 $(echo "$FILES" | head -n 1))
echo "$HEADER" > "$OUTPUT_FILE"

for file in $FILES; do
    tail -n +2 "$file" >> "$OUTPUT_FILE"
done

echo "data saved to $OUTPUT_FILE."