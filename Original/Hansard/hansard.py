'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 01/12/2024
'''

from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
from botocore.exceptions import ClientError
import PyPDF2

session = requests.Session()
# Base URL for the Hansard site
base_url = 'https://hansard.parliament.uk/pdf/commons/'

# Function to build the full URL for a given date
def build_url_for_date(date):
    return f"{base_url}{date}"

url  = build_url_for_date('2024-01-11')
print(url)


import boto3
import io

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

    #When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')
    # # # When using IAM roles, boto3 retrieves credentials from the instance metadata
    # s3_client = boto3.client('s3')


    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True


import boto3
import logging
from botocore.exceptions import ClientError

def upload_pdf_to_s3(pdf_binary, bucket, object_name):
    """
    Upload a PDF to an S3 bucket.

    :param pdf_binary: Binary stream of the PDF file
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: True if the PDF was uploaded, else False
    """
    # When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')
    # # When using IAM roles, boto3 retrieves credentials from the instance metadata
    # s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=pdf_binary)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#Generate a list of dates
import datetime
start_date = datetime.date(2000, 1, 1)
end_date = datetime.date(2024, 1, 12)
delta = datetime.timedelta(days=1)
dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += delta



Hansard_NoSitting = []
bucket_name = 'myukdata'
folder_path = 'Hansard'
# Create a list of file names with the name formatted as 'Hansard_YYYY-MM-DD.txt'
object_names = [f"{folder_path}/Hansard_{date.strftime('%Y-%m-%d')}.txt" for date in dates]
print(len(object_names))


    
for date in dates:
    print(date)
    hansard_url = build_url_for_date(date)
    response_pdf = requests.get(hansard_url, impersonate='chrome110')
    if response_pdf.status_code == 200:
        print(f"Hansard link found:{hansard_url} for {date}")
        # Extract binary content from response
        pdf_binary_content = response_pdf.content
        # Upload the DataFrame to S3
        if upload_pdf_to_s3(pdf_binary_content, bucket_name, f"{folder_path}/Hansard_{date.strftime('%Y-%m-%d')}.pdf"):
            print(f"PDF uploaded successfully for {date}")
    else:
        print(response_pdf.status_code)
        Hansard_NoSitting.append(date.strftime('%Y-%m-%d'))
        print(f"Text download failed for {date}")
Hansard_NoSitting = pd.DataFrame(Hansard_NoSitting)
if Hansard_NoSitting.empty == False:
    Hansard_NoSitting.columns = ['Date']
upload_df_to_s3(Hansard_NoSitting, bucket_name, f"{folder_path}/Hansard_NoSitting.csv")

