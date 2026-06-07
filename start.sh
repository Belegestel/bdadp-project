docker pull adamgput/hadoop-pyspark-put:1.0
docker network create --driver=bridge hadoop
docker run -itd --name hadoop-master --hostname hadoop-master -p 9864:9864 -p 9870:9870 -p 8088:8088 -p 8888:8888 --net=hadoop adamgput/hadoop-pyspark-put:1.0
docker run -itd --name hadoop-slave1 --hostname hadoop-master --net=hadoop adamgput/hadoop-pyspark-put:1.0
docker run -itd --name hadoop-slave2 --hostname hadoop-master --net=hadoop adamgput/hadoop-pyspark-put:1.0

