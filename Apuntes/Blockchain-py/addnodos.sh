curl -X POST 'http://10.5.0.4:3000/addnode' -H 'Content-Type: application/json' -d '{"nodes" :"http://10.5.0.5:3000"}'

curl -X POST 'http://10.5.0.5:3000/addnode' -H 'Content-Type: application/json' -d '{"nodes" :"http://10.5.0.4:3000"}'
