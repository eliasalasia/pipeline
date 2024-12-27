# Pipeline de Datos para Análisis de Telecomunicaciones
## Descripción del Proyecto
Este proyecto simula el procesamiento de datos de telecomunicaciones para una empresa del sector. Los datos se almacenan en un Data Lake (Amazon S3), se transforman con AWS Glue, se cargan en un Data Warehouse (Amazon Redshift) para su análisis, y se realizan consultas ad-hoc usando Amazon Athena. Los logs de ejecución del pipeline se registran en Amazon DynamoDB.

## Servicios Utilizados
Amazon S3: Almacenamiento de datos en formato CSV/JSON.
AWS Glue: Proceso ETL (Extract, Transform, Load) para transformar y cargar datos.
Amazon Redshift: Data Warehouse para el análisis de datos transformados.
Amazon Athena: Consultas ad-hoc directamente sobre los datos en S3.
Amazon DynamoDB: Registro de configuraciones y logs del pipeline.
# Configuración del Proyecto
### Paso 1: Crear un Bucket S3
```bash
aws s3 mb s3://telecom-datalake

### Paso 2: Subir Datos a S3
```bash
aws s3 cp example_data.csv s3://telecom-datalake/data/
Ejemplo del archivo data.csv:
```bash
css
id_cliente,nombre_cliente,servicio,fecha_contrato,estado_contrato,monto
1,Juan Perez,Internet,2024-01-01,Activo,50
2,Ana Lopez,Telefonía,2024-02-15,Activo,40
3,Carlos Gomez,Internet,2024-03-10,Cancelado,50
4,María Díaz,Telefonía,2024-04-05,Activo,30

### Paso 3: Catalogación con AWS Glue
Crear un Crawler en AWS Glue:
Navega a la consola de AWS Glue.
Configura un nuevo crawler llamado telecom-data-crawler con los siguientes detalles:
Fuente de Datos: El bucket telecom-datalake.
Rol de IAM: Crea uno con permisos para Glue y S3.
Destino: Glue Data Catalog.
Ejecuta el crawler para catalogar los datos almacenados en S3.

### Paso 4: Crear y Ejecutar un Trabajo de Glue
ETL con AWS Glue:
Crear el Script ETL: Crea un archivo glue_etl_script.py con el siguiente contenido:
```bash
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *

 @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer CSV desde S3
df = spark.read.csv('s3a://telecom-datalake/data/data.csv', header=True)

## Transformaciones
transformed = df.dropDuplicates() \
    .withColumn("duracion", col("duracion").cast("double"))

## Guardar resultados en S3
transformed.write.csv('s3a://telecom-datalake/transformed_data.csv', header=True)

job.commit()
Subir el Script a S3:

```bash
aws s3 cp glue_etl_script.py s3://telecom-datalake/scripts/

### Paso 5: Configurar Amazon Redshift
Configurar Redshift Serverless:
Ve a la consola de Amazon Redshift.
Configura un namespace llamado telecom-namespace y un workgroup telecom-workgroup.
Crea una base de datos y una tabla de destino ejecutando el siguiente comando:
sql
```bash
CREATE TABLE telecom_data (
    id_llamada INT,
    numero_origen VARCHAR(20),
    numero_destino VARCHAR(20),
    duracion DOUBLE,
    fecha DATE
);
### Paso 6: Configurar Amazon DynamoDB
Crear la tabla telecom_pipeline_logs:
Ve a la consola de Amazon DynamoDB.
Crea una tabla llamada telecom_pipeline_logs con la clave primaria execution_id (tipo String).
Script para Registrar Logs:
Crea un archivo dynamodb_logger.py con el siguiente contenido:

```bash
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('telecom_pipeline_logs')

def log_execution(status, message):
    table.put_item(
        Item={
            'execution_id': datetime.now().isoformat(),
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    )

## Ejemplo de cómo llamar a la función para registrar un log
log_execution('Success', 'Pipeline executed successfully')

### Paso 7: Ejecutar Consultas en Athena
## Configurar y Ejecutar Consultas en Athena:
Ve a la consola de Amazon Athena.
Configura el bucket telecom-datalake como fuente de datos.
Crea consultas para analizar los datos. Por ejemplo:
sql
```bash
SELECT * FROM telecom_data LIMIT 10;

## Scripts Utilizados
glue_etl_script.py: Script de Glue para transformar y cargar datos.
dynamodb_logger.py: Script para registrar logs en DynamoDB.
