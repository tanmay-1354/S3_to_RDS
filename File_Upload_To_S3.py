import boto3

# AWS credentials and region
aws_access_key = 'your_access_key'
aws_secret_key = 'your_secret_key'
region_name = 'your_region'

# S3 bucket and file details
bucket_name = 'your_bucket_name'
file_path = 'path_to_your_local_csv_file.csv'
s3_key = 'destination_s3_key/filename.csv'

# Create an S3 client
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

# Upload the file to S3
try:
    response = s3_client.upload_file(file_path, bucket_name, s3_key)
    print(f"File uploaded successfully to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Error uploading file: {e}")
