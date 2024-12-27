from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Inicializar Spark
spark = SparkSession.builder \
    .appName("TelecomETL") \
    .getOrCreate()

# Leer CSV
df = spark.read.csv('data.csv', header=True)

# Transformaciones
transformed = df.dropDuplicates() \
    .withColumn("ingreso_mensual", col("monto").cast("double"))

# Guardar resultados
transformed.write.csv('transformed_data.csv', header=True)