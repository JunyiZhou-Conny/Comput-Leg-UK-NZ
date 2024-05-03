import boto3
import pandas as pd
import io

# Example DataFrame
# final_df = pd.DataFrame(data)

# Convert DataFrame to CSV format in-memory
csv_buffer = io.StringIO()
final_df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)  # Move the pointer to the start of the stream

def upload_df_to_s3(buffer, bucket, object_name):
    """
    Upload a DataFrame buffer to an S3 bucket.

    :param buffer: Buffer containing DataFrame in CSV format
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: True if the buffer was uploaded, else False
    """
    s3_client = boto3.client('s3')
    try:
        # Put the object in S3
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True


bucket_name = 'your-s3-bucket-name'
object_name = 'BillsLatestStage_ID.csv'

# Upload DataFrame
upload_success = upload_df_to_s3(csv_buffer, bucket_name, object_name)
if upload_success:
    print(f"Uploaded DataFrame to {bucket_name}/{object_name}")
else:
    print(f"Failed to upload DataFrame")
