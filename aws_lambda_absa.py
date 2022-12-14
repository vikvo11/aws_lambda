import boto3

iam = boto3.client('iam')


def lambda_handler(event, context):

    # Get the object from the event
    object = event['Records'][0]['s3']['object']
    user_id = event['Records'][0]['userIdentity']['principalId']
    
    try:
        response_iam = iam.get_account_authorization_details(Filter=['User'])
        user_name='Unknown'
        for user in response_iam['UserDetailList']:
            if user['UserId']== user_id.replace('AWS:',''): 
                user_name=user['UserName']
        size = size=object['size'] / 1024
        
        #Create custom metrics
        cloudwatch = boto3.client('cloudwatch')
        response_cloudwatch = cloudwatch.put_metric_data(
            MetricData = [
                {
                    'MetricName': 'size',
                    'Dimensions': [
                        {
                            'Name': user_name,
                            'Value': user_name
                        },
                    ],
                    'Unit': 'None',
                    'Value': size
                },
            ],
            Namespace = 'CodingTest'
        )
        return response_cloudwatch 

    except Exception as e:
        print(e)
        print('Error')
        raise e