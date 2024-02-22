'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 02/11/2024
'''
#Importing the necessary libraries
from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
from botocore.exceptions import ClientError
import fitz
import boto3
import io
import logging
import datetime

# Function to upload a file to an S3 bucket
def upload_txt_to_s3(txt_binary, bucket, object_name):
    """
    Upload a txt to an S3 bucket.

    :param txt_binary: Binary stream of the txt file
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: True if the txt was uploaded, else False
    """
    # When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')
    # # When using IAM roles, boto3 retrieves credentials from the instance metadata
    # s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=txt_binary)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#Generate a list of dates
start_date = datetime.date(2014, 12, 4)
end_date = datetime.date(2024, 2, 11)
delta = datetime.timedelta(days=1)
dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += delta


#Prepare the S3 bucket and folder
bucket_name = 'myukdata'
folder_path = 'Hansard_txt'


# Generate a list of URL that does not have a sitting
Hansard_NoSitting = []


# Set up a request session
session = requests.Session()


# Base URL for the Hansard site
base_url = 'https://hansard.parliament.uk/pdf/commons/'


# Function to build the full URL for a given date
def build_url_for_date(date):
    return f"{base_url}{date}"   
 

for date in dates:
    print(date)
    hansard_url = build_url_for_date(date)
    response_pdf = requests.get(hansard_url, impersonate='chrome110')
    print(response_pdf.status_code)
    if response_pdf.status_code != 200:
        print(f"No Hansard link found for {date}")
        Hansard_NoSitting.append(date.strftime('%Y-%m-%d'))
    if response_pdf.status_code == 200:
        print(f"Hansard link found:{hansard_url} for {date}")
        # Extract binary content from response
        pdf_binary_content = response_pdf.content
        # Turn the binary content into a file-like object
        pdf_file = io.BytesIO(pdf_binary_content)
        # Create a PdfReader object
        pdf_reader = fitz.open("pdf",pdf_binary_content)

        # Extract the text from each page of the PDF
        text = ""
        for i in range(len(pdf_reader)):
            text += pdf_reader[i].get_text()

        # Get text without linebreaks
        text = text.replace("\n", " ")
        # Save the extracted text to a text file
        text_file_path = f"Hansard_{date.strftime('%Y-%m-%d')}.txt"
        
        with open(text_file_path, "w") as text_file:
            text_file.write(text)

        # Upload the text_files to S3
        if upload_txt_to_s3(txt_binary=text, bucket=bucket_name, object_name=f"{folder_path}/Hansard_{date.strftime('%Y-%m-%d')}.txt"):
            print(f"Text uploaded successfully for {date}")
        else:
            # Add the date to the list of dates with no sitting
            Hansard_NoSitting.append(date.strftime('%Y-%m-%d'))
            print(f"Text upload failed for {date}")

#A function to upload a DataFrame to an S3 bucket as CSV, particularly for the Hansard_NoSitting list
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

Hansard_NoSitting = pd.DataFrame(Hansard_NoSitting)
if Hansard_NoSitting.empty == False:
    Hansard_NoSitting.columns = ['Date']
upload_df_to_s3(Hansard_NoSitting, bucket_name, f"{folder_path}/Hansard_NoSitting.csv")

