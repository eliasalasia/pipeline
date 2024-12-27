# Pipeline de Datos para Análisis de Telecomunicaciones

## Descripción del Proyecto
Este proyecto simula el procesamiento de datos de telecomunicaciones, utilizando servicios de AWS para construir un pipeline de datos. Los datos se almacenan en un Data Lake (S3), se transforman con AWS Glue, se cargan en un Data Warehouse (Redshift), y se analizan con Athena. Los logs de ejecución se registran en DynamoDB.

## Servicios Utilizados
- Amazon S3
- AWS Glue
- Amazon Redshift
- Amazon Athena
- Amazon DynamoDB

## Configuración del Proyecto
### Paso 1: Crear un Bucket S3
```bash
aws s3 mb s3://telecom-datalake

## Paso 2: Subir Datos a S3
aws s3 cp example_data.csv s3://telecom-datalake/data/
## Paso 3: Configurar AWS Glue
Crear un crawler y ejecutar para catalogar los datos.

## Paso 4: Crear y Ejecutar un Trabajo de Glue
Subir glue_etl_script.py a S3 y configurar el trabajo en AWS Glue.

## Paso 5: Configurar Amazon Redshift
Crear un namespace, workgroup, base de datos y tabla.

## Paso 6: Configurar Amazon DynamoDB
Crear la tabla telecom_pipeline_logs.

## Paso 7: Ejecutar Consultas en Athena
Ejecutar consultas para analizar los datos transformados.

Scripts Utilizados
glue_etl_script.py: Script de Glue para transformar y cargar datos.

dynamodb_logger.py: Script para registrar logs en DynamoDB.