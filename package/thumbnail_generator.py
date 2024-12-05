import logging
import boto3
from io import BytesIO
from PIL import Image
import os

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

def create_thumbnail(image, max_dimension):
    """
    Create a thumbnail from an image with specified max dimension.
    Handles different image modes and preserves aspect ratio.
    """
    # Convert to RGB if needed
    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background

    # Resize maintaining aspect ratio
    image.thumbnail((max_dimension, max_dimension))
    return image

def lambda_handler(event, context):
    # Environment Variables
    ORIGINAL_BUCKET = os.environ['ORIGINAL_BUCKET']
    THUMBNAIL_BUCKET = os.environ['THUMBNAIL_BUCKET']
    MAX_THUMBNAIL_SIZE = int(os.environ['MAX_THUMBNAIL_SIZE'])

    try:
        # Extract S3 event details
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        source_key = record['object']['key']

        # Validate source matches original bucket
        if source_bucket != ORIGINAL_BUCKET.split('/')[0]:
            raise ValueError(f"Unexpected source bucket: {source_bucket}")

        # Determine thumbnail path
        thumbnail_key = source_key.replace('original', 'thumbnails')

        # Fetch and process image
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        image_bytes = response['Body'].read()
        
        with Image.open(BytesIO(image_bytes)) as img:
            thumbnail = create_thumbnail(img, MAX_THUMBNAIL_SIZE)
            
            # Save thumbnail
            thumb_bytes = BytesIO()
            thumbnail.save(thumb_bytes, format='JPEG', quality=85)
            thumb_bytes.seek(0)

            # Upload to S3
            s3.put_object(
                Bucket=THUMBNAIL_BUCKET.split('/')[0], 
                Key=thumbnail_key, 
                Body=thumb_bytes, 
                ContentType='image/jpeg'
            )

        logger.info(f"Thumbnail created: {thumbnail_key}")
        return {
            'statusCode': 200,
            'body': f"Thumbnail successfully generated: {thumbnail_key}"
        }

    except Exception as e:
        logger.error(f"Thumbnail generation error: {str(e)}")
        raise