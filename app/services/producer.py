import pika
import json


url = 'amqps://weitflya:if6bVbMbsqJeejYscqx9BHjJNGXOJ2Py@stingray.rmq.cloudamqp.com/weitflya'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    """Send request with transaction_id to delete the group
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='apiconsumer_cluster',
                          body=json.dumps(body), properties=properties)
