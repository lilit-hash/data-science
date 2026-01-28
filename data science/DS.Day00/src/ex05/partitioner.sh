#!/bin/sh
INPUT_FILE="../ex03/hh_positions.csv"

if [ ! -f "$INPUT_FILE" ]; then
    echo "file not found"
    exit 1
fi

HEADER=$(head -n 1 "$INPUT_FILE")
tail -n +2 "$INPUT_FILE" | while IFS= read -r line; do
    created_at=$(echo "$line" | cut -d'"' -f4 | cut -d'T' -f1)
    if [ ! -f "${created_at}.csv" ]; then
        echo "$HEADER" > "${created_at}.csv"
    fi
    echo "$line" >> "${created_at}.csv"
done

echo "well done"