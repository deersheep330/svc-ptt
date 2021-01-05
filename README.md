# PttTrends Service

#### run without docker
```
python main.py
```

#### start a docker service
```
docker-compose build
docker-compose push
docker stack deploy -c docker-compose.yml ptt
```
#### uninstall all pip packages
```
pip uninstall -r requirements.txt
```
