'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 03/14/2024
'''

from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
from botocore.exceptions import ClientError
import PyPDF2
import io

import boto3
import logging
from botocore.exceptions import ClientError


def download_file_from_s3(bucket, object_name, local_file_name):
    """
    Download a file from S3 to the local file system.

    :param bucket: Name of the S3 bucket
    :param object_name: S3 object name
    :param local_file_name: Local file name to save the downloaded file
    """
    # # When using IAM roles, boto3 retrieves credentials from the instance metadata
    # s3_client = boto3.client('s3')

    #When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')

    s3_client.download_file(bucket, object_name, local_file_name)

bucket_name = 'myukdata'
s3_file_name = 'Original/Publication/Publication_Modified.csv'
local_file = 'Publication_Modified.csv'

download_file_from_s3(bucket_name, s3_file_name, local_file)



def upload_pdf_html_to_s3(binary, bucket, object_name):
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
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=binary)
    except ClientError as e:
        logging.error(e)
        return False
    return True


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


# Import Publication_modified.csv
import pandas as pd
df = pd.read_csv('Publication_Modified.csv')
df['objectNames'] = df['billId'].astype(str) + '_' + df['publicationTypeId'].astype(str) + '_' + df['id'].astype(str) + '_' + df['fileType']



# s3://myukdata/Original/Publication/Publication_PDF/
bucket_name = 'myukdata'
folder_path_pdf = 'Original/Publication/Publication_PDF'
folder_path_html = 'Original/Publication/Publication_HTML'
folder_path_failed = 'Original/Publication'

failed_object = []
for i in range(len(df)):
    link = df.loc[i, 'links']
    objectName = df.loc[i, 'objectNames']
    print(link, objectName)

    # Check if the link exists
    if link:
        # Check if the link is a PDF or HTML, upload them into 2 separate folders
        if '.pdf' in link:
            response_pdf = requests.get(link, impersonate='chrome110')
            if response_pdf.status_code == 200:
                print(f"PDF downloaded for {objectName}")
                response_pdf = requests.get(link, impersonate='chrome110')
                # Extract binary content from response
                pdf_binary_content = response_pdf.content
                # Upload the DataFrame to S3
                upload_pdf_html_to_s3(pdf_binary_content, bucket_name, f"{folder_path_pdf}/{objectName}.pdf")
            else:
                print(f"PDF download failed for {objectName}")
                failed_object.append(objectName)
        elif '.html' in link:
            response_html = requests.get(link, impersonate='chrome110')
            if response_html.status_code == 200:
                print(f"HTML downloaded for {objectName}")
                response_html = requests.get(link, impersonate='chrome110')
                # Extract binary content from response
                html_binary_content = response_html.content
                # Upload the DataFrame to S3
                upload_pdf_html_to_s3(html_binary_content, bucket_name, f"{folder_path_html}/{objectName}.html")
            else:
                print(f"HTML download failed for {objectName}")
                failed_object.append(objectName)



# Save failed_object to S3
failed_object = pd.DataFrame(failed_object)
if failed_object.empty == False:
    failed_object.columns = ['objectName']
    upload_df_to_s3(failed_object, bucket_name, f"{folder_path_failed}/failed_object.csv")







