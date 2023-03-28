curl -X POST 'http://localhost:5000/addnode' -H 'Content-Type: application/json' -d '{"nodes" :"http://localhost:5001"}'

curl -X POST 'http://localhost:5001/addnode' -H 'Content-Type: application/json' -d '{"nodes" :"http://localhost:5000"}'
