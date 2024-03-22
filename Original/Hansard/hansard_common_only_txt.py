from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
from botocore.exceptions import ClientError
from curl_cffi.requests.errors import RequestsError


session = requests.Session()
# Base URL for the Hansard site
base_url = 'https://hansard.parliament.uk/html/commons'

# Function to build the full URL for a given date
def build_url_for_date(date):
    return f"{base_url}/{date}/CommonsChamber"



def text_download(url):
    base_url = 'https://hansard.parliament.uk'
    try:
        response = session.get(url, impersonate='chrome110')

    
    except RequestsError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return []
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return []
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    text_link = soup.find('a', class_='icon-link', href=lambda h: h and 'GetDebateAsText' in h)
    if text_link is None:# If there is no text link, return an empty list, and print a message
        return []
    full_url = base_url + text_link['href']
    return full_url



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
import io

def upload_text_to_s3(text, bucket, object_name):
    """
    Upload a text to an S3 bucket.

    :param text: Text to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: True if the text was uploaded, else False
    """
    # Create a buffer
    text_buffer = io.StringIO()
    text_buffer.write(text)

    # Move to the start of the buffer
    text_buffer.seek(0)

    # When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')

    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=text_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True



#Generate a list of dates
import datetime
start_date = datetime.date(2000, 1, 1)
end_date = datetime.date(2024, 3, 17)
delta = datetime.timedelta(days=1)
dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += delta



Hansard_Failed = []
Hansard_NoText = []
bucket_name = 'myukdata'
folder_path = 'Hansard_Common_Chambers'



    
for date in dates:
    # Build the URL for the date
    hansard_url = build_url_for_date(date)

    # Get the text link for the date, this is the download text button on the top left of the page
    text_link = text_download(hansard_url)

    if text_link == []:
        Hansard_NoText.append(date.strftime('%Y-%m-%d'))
        print(f"No texts found for download {date}")

    else:
        print(f"Text link found:{text_link} for {date}")
        response_text = requests.get(text_link, impersonate='chrome110')
        if response_text.status_code == 200:
            print(f"Text downloaded for {date}")
            # Upload the DataFrame to S3
            upload_text_to_s3(response_text.text, bucket_name, f"{folder_path}/Hansard_{date.strftime('%Y-%m-%d')}.txt")
        else:
            print(f"Text download failed for {date}")
            Hansard_Failed.append(date.strftime('%Y-%m-%d'))

Hansard_Failed = pd.DataFrame(Hansard_Failed)
Hansard_NoText = pd.DataFrame(Hansard_NoText)
if Hansard_Failed.empty == False:
    Hansard_Failed.columns = ['Date']
if Hansard_NoText.empty == False:
    Hansard_NoText.columns = ['Date']
upload_df_to_s3(Hansard_Failed, bucket_name, f"{folder_path}/Hansard_FailedS3.csv")
upload_df_to_s3(Hansard_NoText, bucket_name, f"{folder_path}/Hansard_NoSitting.csv")




