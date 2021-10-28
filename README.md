# auth-server-sample

```
docker-compose up -d
docker exec -it server bash

# docker[server]
pip install -r requirements.txt
uvicorn main:app --port 8080 --host 0.0.0.0 --reload
```

## テスト

View  
http://localhost:8080/authorization?client_id=client001&response_type=code  

```
curl -sS localhost:8080/v1/token -H "Authorization: Basic $(echo client:secret | base64)" | jq .

curl -sS -u client:secret localhost:8080/v1/token?grant_type=client_credentials | jq .

curl -sS localhost:8080/v1/user -H "Authorization: Bearer static.token" | jq .
```
