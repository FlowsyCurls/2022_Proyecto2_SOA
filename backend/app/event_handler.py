# pika: rabbitmq client library to rend or receive messages from our message broker
import pika
import os
from api import create_record

# This functinon listen to the connection and acts when a message is added to the respective queue.
# INPUT: body : message


def on_message_received(ch, method, properties, body):
    print(f'\n\n⭐ received: "{body}"')

    # Process the data received
    create_record(body)
    print(f'\n▶ finished processing and acknowledged message')

# This functinon establish a connection (keeps running until the program is finished) with broker and start a channel to receive message from the queue.


def consume():
    # set parameter to establish connection
    host = os.environ['RABBIT_HOST']
    port = os.environ['RABBIT_PORT']
    queue = os.environ['RABBIT_CONSUMER_QUEUE']
    # queue = 'testing'

    # create a connection to the locally running rabbitmq message broker
    # connection_parameters = pika.ConnectionParameters('localhost')
    connection_parameters = pika.ConnectionParameters(host=host,port=port)

    # save connection by passing our connection parameters
    connection = pika.BlockingConnection(connection_parameters)

    # store a default channel
    channel = connection.channel()  # There could be multiples channels

    # declare a queue in the channel
    channel.queue_declare(queue=queue)

    # use basic consume method to consume of the queue
    channel.basic_consume(queue=queue, auto_ack=True,
                          on_message_callback=on_message_received)

    # tell channel to start consuming
    print("\n⌛ Starting consuming...\n")
    channel.start_consuming()
