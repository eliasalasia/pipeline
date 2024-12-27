import boto3

athena_client = boto3.client('athena')

def run_query():
    query = """
    SELECT servicio, COUNT(*) as total_clientes, 
           SUM(monto) as ingreso_total
    FROM telecom_data
    GROUP BY servicio
    """
    
    response = athena_client.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': 's3://tu-bucket/athena_results/'
        }
    )
    return response['QueryExecutionId']