'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/19/2023
'''
import boto3
from botocore.exceptions import ClientError
import requests
import time
import json
import math
import sys
import pandas as pd


def get(MEM_ID):
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

    #Appending each response to this results list
    results = []


    url = f"https://members-api.parliament.uk/api/Members/{MEM_ID}"
    response = requests.get(url)

    #Currently, the success code is 200 from "https://members-api.parliament.uk/index.html"
    if response.status_code == 200:

        #Parse the JSON response into a Python dictionary
        data = response.json()

        #Append the data to the results list
        results.append(data)

    elif response.status_code == 404:
        #Append the error message to the errors list
        errors_404 = MEM_ID

        print(f"Error fetching data for ID as it is not found{MEM_ID}")
        # Optionally, sleep for longer if an error occurs to give the server a break
        # As far as I know, the server does not have a rate limit
        time.sleep(1)
    
    elif response.status_code == 500:
        errors_500 = MEM_ID

        print(f"Error fetching data for ID due to server error{MEM_ID}")

    return results, errors_404, errors_500

#There is not limit for UK Parliament API for now, we can skip settiing the API key or the Entry per request
#ENTRIES_PER_REQUEST = 250
#API_KEY = get_key(int(sys.argv[2]))


MEM_ID_START =  1
MEM_ID_END = 5020



# Get the data and normalize the json file
final = []
final_404 = []
final_500 = []

for ID in range(MEM_ID_START, MEM_ID_END + 1):
    member, errors_404, errors_500 = get(MEM_ID = ID)
    print(ID)
    if member is not None:
        df_all = pd.json_normalize(member)
        #df_all = df_all.replace(r'\n', ' ', regex=True)
        #df_all = df_all.replace(r'\r', ' ', regex=True)
        #df_all = df_all.replace(r'\t', ' ', regex=True)
        final.append(df_all)
    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)

#Concatenate all the lists into one dataframe
final_df = pd.concat(final, ignore_index=True)



#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["memberID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["memberID"]


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
folder_path = 'Member'
file_names = ['Member.csv','Member_404.csv','Member_500.csv']  # Replace with your desired S3 object names
# Create full object names with folder path
object_names = [f"{folder_path}/{file_name}" for file_name in file_names]

# Example DataFrames
dfs = [final_df, final_df_404, final_df_500]


# Loop over DataFrames and upload each
for df, object_name in zip(dfs, object_names):
    upload_success = upload_df_to_s3(df, bucket_name, object_name)
    if upload_success:
        print(f"Uploaded {object_name} to {bucket_name}")
    else:
        print(f"Failed to upload {object_name}")




#Store the 2 error lists in a csv file
# final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_404.csv", index=False)
# final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_500.csv", index=False)
# final_df.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member.csv", index=False)

