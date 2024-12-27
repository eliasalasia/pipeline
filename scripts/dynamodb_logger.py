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

# Ejemplo de cómo llamar a la función para registrar un log
log_execution('Success', 'Pipeline executed successfully')
