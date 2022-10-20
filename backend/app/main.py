from event_handler import consume
from api import run
from time import sleep
from threading import Thread

# Create thread to run api and run the consumer function
if __name__ == '__main__':
    Thread(target=run).start()
    sleep(5)
    Thread(target=consume).start()
