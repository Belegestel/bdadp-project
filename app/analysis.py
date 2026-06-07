import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

def get_spark_session():
    spark = SparkSession.builder \
        .appName("CarDataAnalysisApp") \
        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    data = spark.read.csv("hdfs://hadoop-master:9000/data/data.csv", header=True, inferSchema=True)
    os.system('cls' if os.name == 'nt' else 'clear')
    return spark, data

def query(df, *data):
    # Data = [(col1, '+-'), ...] (column name, asc/desc)
    colnames, directionality = zip(*data)
    return df.select(*colnames, 'name', 'model_year', 'origin') \
            .orderBy(*[
                F.col(name).asc() if dir == '+' else F.col(name).desc() 
                for name, dir in zip(colnames, directionality)
            ])



if __name__ == "__main__":
    print("Initializing Spark Engine... Please wait a moment.")
    spark = get_spark_session()
    df = load_data(spark)
    
    spark.stop()
