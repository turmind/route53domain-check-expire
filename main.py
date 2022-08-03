import json
import os
import json
import boto3
import datetime

def lambda_handler(event, context):
    expire_notify_day = int(os.getenv("Expire_Notify_Day"))
    print("get domain expire greater than ", expire_notify_day, " days")
    client = boto3.client('route53domains', region_name='us-east-1')
    
    response = client.list_domains(
        SortCondition={
            'Name': 'Expiry',
            'SortOrder': 'ASC'
        },
        MaxItems=100
    )

    dict = {"domains": ""}
    now = datetime.datetime.now()
    
    for Domain in response['Domains'] :
        interval = Domain['Expiry'].replace(tzinfo=None) - now
        if interval.days > expire_notify_day :
            break
        if dict["domains"] > "":
            dict["domains"] += "\n"
        dict["domains"] += Domain["DomainName"] + "有效期" + str(interval.days) + "天"
    
    event_client = boto3.client('events')

    response = event_client.put_events(
        Entries=[
            {
                'Source': 'Route53Domain.Expire.Notify',
                'DetailType': 'Route53 Domain Expire Notify',
                'Detail': json.dumps(dict),
                'EventBusName': 'default',
            },
        ],
    )

    return