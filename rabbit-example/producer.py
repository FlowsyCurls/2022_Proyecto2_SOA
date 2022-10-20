# pika: rabbitmq client library to rend or receive messages from our message broker
import pika
import time
import random

# create a connection to my locally running rabbitmq message broker
connection_parameters = pika.ConnectionParameters('localhost')

# save connection by passing our connection parameters
connection = pika.BlockingConnection(connection_parameters)

# store a default channel
channel = connection.channel()

# declare a queue in the channel
channel.queue_declare(queue='letterbox')

# set a message identifier
messageId = 1

while(True):
  # message we want to publish to the exchange
  message = f"Sending Message Id: {messageId}"
  
  # publish message by using a default exchange (empty string)
  channel.basic_publish(exchange='', routing_key='letterbox', body=message)

  print(f"sent message: {message}")
  
  time.sleep(random.randint(1, 4))

  messageId+=1