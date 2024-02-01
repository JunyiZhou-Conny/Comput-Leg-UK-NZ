'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/19/2023
'''



import boto3
from botocore.exceptions import ClientError
import pandas as pd
import json
import requests
import csv
import numpy as np
import time

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
s3_file_name = 'Bills/BillAllStages/BillsAllStages.csv'
local_file = 'BillAllStages.csv'

download_file_from_s3(bucket_name, s3_file_name, local_file)

# Read into pandas DataFrames
df = pd.read_csv(local_file)
temp = df


#Extract the first 2 columns of temp into a dataframe called amendment
amendment = temp.iloc[:,0:2]

billId_list = [int (num) for num in amendment.iloc[:, 0].tolist()]
stageId_list =[int (num) for num in amendment.iloc[:, 1].tolist()]
print(len(billId_list))
print(len(stageId_list))




def get(BillID, StageID):
    #These indicators are not used in this current version of script to extract member data
    #Indicator for whether the request is complete/ Exit condition out of the while loop
    isComplete = False

    #Specify the starting point for th next chunk of data in each new request
    offset = 0

    #Iteration number
    iteration = 1

    #Total number of entries
    total_entries = 0

    #Store the error ID, indicating that the response is not found
    errors_404 = 0

    #Store the error ID, indicating there exists an internal server error
    errors_500 = 0

    #Store the error list, indicating that the request is bad
    errors_400 = 0

    #Appending each response to this results list
    results = []


    url = f"https://bills-api.parliament.uk/api/v1/Bills/{BillID}/Stages/{StageID}/Amendments"
    response = requests.get(url)

    #Currently, the success code is 200 from "https://bills-api.parliament.uk/index.html"
    if response.status_code == 200:

        #Parse the JSON response into a Python dictionary
        data = response.json()

        #Append the data to the results list
        results.append(data)

    elif response.status_code == 404:
        #Append the error message to the errors list
        errors_404 = [BillID, StageID]

        print(f"Error fetching data for ID as it is not found {[BillID, StageID]}")
        # Optionally, sleep for longer if an error occurs to give the server a break
        # As far as I know, the server does not have a rate limit
        time.sleep(1)
    
    elif response.status_code == 500:
        errors_500 = [BillID, StageID]


        print(f"Error fetching data for ID due to server error {[BillID, StageID]}")

    elif response.status_code == 400:
        errors_400 = [BillID, StageID]


        print(f"Error fetching data for ID due to bad request {[BillID, StageID]}")

    return results, errors_404, errors_500, errors_400




import requests
import time
final = []
final_noamen = []
final_404 = []
final_500 = []
final_400 = []
for BillID, StageID in zip(billId_list, stageId_list):
        bills, errors_404, errors_500, errors_400 = get(BillID, StageID)
        print(BillID, StageID)
        if errors_404 != 0:
                final_404.append(errors_404)
        elif errors_500 != 0:
                final_500.append(errors_500)
        elif errors_400 != 0:
            final_400.append(errors_400)
        elif pd.json_normalize(bills[0],record_path=['items']).empty:
            final_noamen.append([BillID, StageID])
        elif bills is not None:
                norm = pd.json_normalize(bills[0], record_path=['items'])
                final.append(norm)

final_df = pd.concat(final, ignore_index=True)


#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_df_400 = pd.DataFrame(final_400)
final_df_noamen = pd.DataFrame(final_noamen)


#Make 2 columns, one for the BillID and one for the StageID
if len(final_df_404) != 0:
    final_df_404.columns = ["ID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["ID"]
if len(final_df_400) != 0:
    final_df_400.columns = ["ID"]
if len(final_df_noamen) != 0:
    final_df_noamen.columns = ["BillID", "StageID"]



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

    # # When using IAM roles, boto3 retrieves credentials from the instance metadata
    # s3_client = boto3.client('s3')

    #When setting up credentials locally, use the following code
    session = boto3.Session()
    s3_client = session.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True



bucket_name = 'myukdata'
folder_name = 'Amendment' 
# Example DataFrames
dfs = [final_df, final_df_noamen, final_df_404, final_df_500, final_df_400]  
file_names = ['Amendment.csv','AmendmentNoAmen.csv','Amendment404.csv', 'Amendment500.csv', 'Amendment400.csv']  
object_names = [f"{folder_name}/{file_name}" for file_name in file_names] 

# Loop over DataFrames and upload each
for df, object_name in zip(dfs, object_names):
    upload_success = upload_df_to_s3(df, bucket_name, object_name)
    if upload_success:
        print(f"Uploaded {object_name} to {bucket_name}")
    else:
        print(f"Failed to upload {object_name}")
