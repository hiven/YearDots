import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://redsnips_user:5giaSr1exfKwJQ1krdhpmuMjAouydCmu@dpg-cp6e8do21fec738guak0-a.oregon-postgres.render.com/redsnips'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    POSTS_PER_PAGE = 10
    

    
    PREPROCESS_BUCKET = 'originalmedia'
    POSTPROCESS_BUCKET = 'processedmedia'

    PROCESSING_QUEUE = 'https://sqs.us-east-1.amazonaws.com/109633410385/ProcessObject.fifo'
