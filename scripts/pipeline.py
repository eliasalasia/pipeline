import boto3

# Crear un cliente de S3
s3_client = boto3.client('s3')

# Listar los buckets disponibles
response = s3_client.list_buckets()

# Mostrar los nombres de los buckets
for bucket in response['Buckets']:
    print(f'Bucket encontrado: {bucket["Name"]}')
