#!/bin/sh
INPUT_FILE="../ex02/hh_sorted.csv"
OUTPUT_FILE="hh_positions.csv"

HEADER=$(head -n 1 "$INPUT_FILE")

echo "$HEADER" > "$OUTPUT_FILE"
tail -n +2 "$INPUT_FILE" | awk -F'"' -v OFS='"' '
{
    positions = ""
    if ($6 ~ /Junior/) positions = "Junior"
    if ($6 ~ /Middle/) positions = (positions ? positions "/" : "") "Middle"
    if ($6 ~ /Senior/) positions = (positions ? positions "/" : "") "Senior"

    $6 = (positions ? positions : "-")
    print
}' >> "$OUTPUT_FILE"

echo "data saved to $OUTPUT_FILE"