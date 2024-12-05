# AWS Lambda Thumbnail Generator

## Overview
Serverless Lambda function for generating thumbnails from images uploaded to S3 buckets.

## Requirements
- Python 3.9
- AWS Lambda
- boto3
- Pillow (PIL)

## Features
- Converts images to thumbnails
- Supports multiple image formats
- Preserves aspect ratio
- Configurable max thumbnail size

## Environment Variables
- `MAX_THUMBNAIL_SIZE`: Max thumbnail size (pixels)
- `ORIGINAL_BUCKET`: Source S3 bucket path
- `THUMBNAIL_BUCKET`: Destination S3 bucket path

## Deployment Configuration
- Runtime: Python 3.9
- Architecture: x86_64
- Handler: `thumbnail_generator.lambda_handler`

## Local Development
```bash
# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create deployment package
zip -r thumbnail_lambda.zip .
```

## Docker Build
```bash
# Build Lambda-compatible package
docker build -t lambda-thumbnail-builder .
docker create --name temp-container lambda-thumbnail-builder
docker cp temp-container:/app/thumbnail_lambda.zip .
docker rm temp-container
```

## Sample Test Event
```json
{
  "Records": [
    {
      "s3": {
        "bucket": {"name": "your-bucket"},
        "object": {"key": "images/original/image.png"}
      }
    }
  ]
}
```

## License
MIT License

## Contributing
PRs welcome. Please open an issue first to discuss proposed changes.
