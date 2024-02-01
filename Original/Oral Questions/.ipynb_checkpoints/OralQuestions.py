from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
from botocore.exceptions import ClientError

session = requests.Session()
# Base URL for the Hansard site
base_url = 'https://hansard.parliament.uk'

# Function to build the full URL for a given date
def build_url_for_date(date):
    return f"{base_url}/commons/{date}"

url  = build_url_for_date('1802-07-02')
print(url)

# Function to get all debate URLs for a given date that include 'OralAnswersToQuestions' in their href
def get_oral_answers_urls_for_date(date):
    url = build_url_for_date(date)
    
    try:
        
        response = session.get(url, impersonate='chrome110')
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
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
    links = soup.find_all('a', class_='card card-section', href=lambda h: h and 'OralAnswersToQuestions' in h)
    if len(links) == 0:
        return []
    full_urls = [base_url + link['href'] for link in links]
    return full_urls

def text_download(url):
    try:
        if url is None:
            return []
        response = session.get(url, impersonate='chrome110')
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
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



#Generate a list of dates
import datetime
start_date = datetime.date(2018, 10, 23)
end_date = datetime.date(2023, 12, 22)
delta = datetime.timedelta(days=1)
dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += delta



OralQuestions_NoOral = []
OralQuestions_NoText = []
bucket_name = 'myukdata'
folder_path = 'OralQuestions'
# Create a list of file names with the name formatted as 'OralQuestions_YYYY-MM-DD.txt'
object_names = [f"{folder_path}/OralQuestions_{date.strftime('%Y-%m-%d')}.txt" for date in dates]
print(len(object_names))


    
for date in dates:
    print(date)
    oral_answers_urls = get_oral_answers_urls_for_date(date)
    if oral_answers_urls == []:
        OralQuestions_NoOral.append(date.strftime('%Y-%m-%d'))
        print(f"No OralQuestions links found for {date}")
    else:
        oral_answers_url = oral_answers_urls[0]
        text_link = text_download(oral_answers_url)
        if text_link == []:
            OralQuestions_NoText.append(date.strftime('%Y-%m-%d'))
            print(f"No texts found for download {date}")
        else:
            print(f"Text link found:{text_link} for {date}")
            response_text = requests.get(text_link, impersonate='chrome110')
            if response_text.status_code == 200:
                print(f"Text downloaded for {date}")
                # Upload the DataFrame to S3
                df = pd.read_csv(io.StringIO(response_text.text), sep='\t')
                upload_df_to_s3(df, bucket_name, f"{folder_path}/OralQuestions_{date.strftime('%Y-%m-%d')}.csv")
            else:
                print(f"Text download failed for {date}")
OralQuestions_NoOral = pd.DataFrame(OralQuestions_NoOral)
OralQuestions_NoText = pd.DataFrame(OralQuestions_NoText)
if OralQuestions_NoOral.empty == False:
    OralQuestions_NoOral.columns = ['Date']
if OralQuestions_NoText.empty == False:
    OralQuestions_NoText.columns = ['Date']
upload_df_to_s3(OralQuestions_NoOral, bucket_name, f"{folder_path}/OralQuestions_NoOral.csv")
upload_df_to_s3(OralQuestions_NoText, bucket_name, f"{folder_path}/OralQuestions_NoText.csv")




