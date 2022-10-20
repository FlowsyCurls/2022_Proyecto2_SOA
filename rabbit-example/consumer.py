# pika: rabbitmq client library to rend or receive messages from our message broker
import pika
import time
import random

def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'received: "{body}", will take {processing_time} to process')
    time.sleep(processing_time)
    
    # tell broker which message we want to acknowledge 
    # (the one we just received not something else) 
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    print(f'finished processing and acknowledged message')

# create a connection to my locally running rabbitmq message broker
connection_parameters = pika.ConnectionParameters('localhost')

# save connection by passing our connection parameters
connection = pika.BlockingConnection(connection_parameters)

# store a default channel
channel = connection.channel()

# declare a queue in the channel
channel.queue_declare(queue='letterbox')

# dispatch mechanism - each consumer will only process a single message at a time
channel.basic_qos(prefetch_count=1)

# use basic consume method to consume of the queue
channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)

print("Starting Consuming")

# tell channel to start consuming
channel.start_consuming()