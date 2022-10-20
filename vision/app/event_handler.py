import pika
import json
import os

# This function establishes a new connection with the broker
# and sends the message to a specific queue.
# INPUT: message : An object containing the analysis of emotions
def produce(message):

    # set parameter to establish connection
    host = os.environ['RABBIT_HOST']
    port = os.environ['RABBIT_PORT']
    queue = os.environ['RABBIT_PRODUCER_QUEUE']
    # queue = 'testing'

    # create a connection to the locally running rabbitmq message broker
    # connection_parameters = pika.ConnectionParameters('localhost')
    connection_parameters = pika.ConnectionParameters(host=host,port=port)

    # save connection by passing our connection parameters
    connection = pika.BlockingConnection(connection_parameters)

    # store a default channel
    channel = connection.channel()  # There could be multiples channels.
    
    # declare a queue in the channel
    channel.queue_declare(queue=queue)
    
    # publish message by using a default exchange (empty string)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    print(f"⭐ sent message:", json.dumps(message,indent=2))

    # close connection
    connection.close()