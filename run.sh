docker compose up -d 
docker exec -it hadoop-master pip install matplotlib 
docker exec -it hadoop-master start-dfs.sh
docker exec -it hadoop-master start-yarn.sh
docker exec -it hadoop-master hdfs dfs -mkdir /data/
docker exec -it hadoop-master hdfs dfs -put /app/data.csv /data/data.csv
docker exec -it hadoop-master python3 /app/main.py
