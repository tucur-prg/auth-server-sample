# auth-server-sample

```
docker-compose up -d
docker exec -it server bash

# docker[server]
pip install -r requirements.txt
uvicorn main:app --port 8080 --host 0.0.0.0 --reload
```

## テスト

登録  
```
curl -sS localhost:8080/user/register -XPOST -d "username=hoge" | jq .
curl -sS localhost:8080/client/register -XPOST -d "client_id=client001" -d "name=hoge" | jq .
```

View  
http://localhost:8080/authorization?client_id=client001&response_type=code&state=123  

```
curl -sS -u client:secret localhost:8080/v1/token -XPOST -d "grant_type=authorization_code" -d "code=???" | jq .

curl -sS -u client:secret localhost:8080/v1/token -XPOST -d "grant_type=client_credentials" | jq .

curl -sS -u client:secret localhost:8080/v1/token -XPOST -d "grant_type=password" -d "username=hoge" -d "password=Passw0rd" | jq .

curl -sS -u client:secret localhost:8080/v1/token -XPOST -d "grant_type=refresh_token" -d "refresh_token=???" | jq .
```
