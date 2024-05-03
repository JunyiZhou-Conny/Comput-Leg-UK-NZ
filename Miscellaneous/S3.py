import boto3

# Create an S3 client
s3 = boto3.client('s3')

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')

# Example: Upload a file to S3
s3.upload_file('path/to/your/file', 'your-bucket-name', 'object-name-on-s3')

# Example: Download a file from S3
s3.download_file('your-bucket-name', 'object-name-on-s3', 'path/to/save/file')
