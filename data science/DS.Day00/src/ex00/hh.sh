
if [ -z "$1" ]; then
  echo "Usage: $0 <search_term>"
  exit 1
fi

SEARCH_TERM="$1"
SEARCH_TERM=$(echo "$SEARCH_TERM" | tr ' ' '+')
API_URL="https://api.hh.ru/vacancies?text=${SEARCH_TERM}&per_page=20"
curl -s "$API_URL" | jq '.' > hh.json
echo "Data saved to hh.json"