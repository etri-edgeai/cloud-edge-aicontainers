curl -X 'POST' \
  'http://deepcase.mynetgear.com:28004/api/edges/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "ETRI New Edge",
  "host": "192.111.111.111",
  "port": 22,
  "description": "Test",
  "access_token": "AAAABBBB",
  "done": true
}'