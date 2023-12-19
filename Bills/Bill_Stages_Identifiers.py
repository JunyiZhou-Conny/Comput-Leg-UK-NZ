'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/18/2023
'''


import boto3
import io
import requests
import pandas as pd
from botocore.exceptions import ClientError



url = "https://bills-api.parliament.uk/api/v1/Stages"
response = requests.get(url)
data = response.json()
final_df = pd.DataFrame(data['items'])




def upload_df_to_s3(df, bucket, object_name):
    """
    Upload a DataFrame to an S3 bucket as CSV.

    :param df: DataFrame to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: True if the DataFrame was uploaded, else False
    """
    # Create a buffer
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Move to the start of the buffer
    csv_buffer.seek(0)

    # Upload the buffer content to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True



bucket_name = 'myukdata'
# Example DataFrames
# Replace with your actual DataFrames
object_name = 'Bills/Bill_Stage_Identifiers.csv'  # Replace with your desired S3 object names
upload_success = upload_df_to_s3(final_df, bucket_name, object_name)
if upload_success:
    print(f"Uploaded {object_name} to {bucket_name}")
else:
    print(f"Failed to upload {object_name}")
