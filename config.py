import os

mongodb = dict(
    host=os.environ['MONGODB_HOST'],
    port=int(os.environ['MONGODB_PORT']),
    name=os.environ['MONGODB_NAME'],
    retry_attempts=1000
)
