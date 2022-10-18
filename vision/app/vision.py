import schedule
import time
from google.cloud import vision 
from google.cloud import storage
from event_handler import produce
from datetime import datetime

# Constants
apikey = "./app/apikey.json"
bucketname = "soa-vision-bucket"

# [START vision_face_detection_gcs]
def detect_emotions_cloud(n):
  """Detects faces in the file located in Google Cloud Storage or the web."""

  # Activate Google vision API using service account key
  client = vision.ImageAnnotatorClient.from_service_account_json(apikey)
  
  # Get GCS bucket
  storage_client = storage.Client.from_service_account_json(apikey)
  bucket = storage_client.bucket(bucketname)
  
  # Get images paths (only one MUST be in bucket)
  blob_list = list(bucket.list_blobs())
  
  # Check if there
  if not blob_list:
    print("Bucket is empty")
    return []
  
  # List to save records
  records = []
  
  # Analize n blobs from the list
  for i in range(0, n):
    
    # when index become bigger than the list
    if len(blob_list) < (i+1):
      break
    
    # Get blob name
    blob_name = blob_list[i].name
    print(f"Image {i+1} - {blob_name} analize.")
    
    # Build image path
    image_path = "gs://{0}/{1}".format(bucketname, blob_name)

    # [START vision_python_migration_image_uri]
    image = vision.Image()
    image.source.image_uri = image_path
    # [END vision_python_migration_image_uri]

    # API face detection response
    response = client.face_detection(image=image)
    
    # Face expression detection
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE','LIKELY', 'VERY_LIKELY')
    acceptable = likelihood_name[3:]
    
    # Get name from document.
    name = blob_name.split('.')[0]
    
    # Get emotions of the first face (default)
    person = { 'name':name, 'emotion':'undetermined' }
    if faces:
      face = faces[0]
      if likelihood_name[face.joy_likelihood] in acceptable: person['emotion']='happy'
      elif likelihood_name[face.sorrow_likelihood] in acceptable: person['emotion']='sad'
      elif likelihood_name[face.anger_likelihood] in acceptable: person['emotion']='angry'
      elif likelihood_name[face.surprise_likelihood] in acceptable: person['emotion']='surprised'
    
    # Set the current date
    now = datetime.now() # current date and time
    person['date'] = now.strftime("%d/%m/%Y %I:%M:%S %p")
    records.append(person)

    # Delete the analyzed image.
    delete_blob(bucket, blob_name)

    if response.error.message:
      raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
          response.error.message))
      
  return records
# [END vision_face_detection_gcs]


def delete_blob(bucket, blob_name):
  """Deletes a blob from the bucket."""
  blob = bucket.blob(blob_name)
  blob.delete()
  # print(f"Blob: {blob_name} deleted.")


# Publish emotions to the queue
def publish_emotions():
  print()
  # how many images to analyze
  n = 3
  json = detect_emotions_cloud(n)
  if json: produce(json)

# Function that handles the routine.
def routine():
  # After every x seconds.
  schedule.every(10).seconds.do(publish_emotions)
  
  # Every 30  or 00:00 time.
  # schedule.every().day.at("00:00").do(publish_emotions)
  
  # Loop
  while True:
    schedule.run_pending()
    time.sleep(1)