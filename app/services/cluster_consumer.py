import pika
import json


url = 'amqps://weitflya:if6bVbMbsqJeejYscqx9BHjJNGXOJ2Py@stingray.rmq.cloudamqp.com/weitflya'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='apiconsumer_cluster')


def callback(ch, method, properties, body):
    """Delete from db with transaction_id
    """
    data = json.loads(body)
    transaction_id = str(data['transaction_id'])
    print(transaction_id)


channel.basic_consume(queue='apiconsumer_cluster',
                      on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
