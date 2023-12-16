'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/15/2023
'''

import requests
import time
import json
import math
import sys
import pandas as pd


def get(SKIP):
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


    url = f"https://questions-statements-api.parliament.uk/api/writtenquestions/questions?tabledWhenTo=2050-01-01&skip={SKIP}&take=20"
    response = requests.get(url)

    #Currently, the success code is 200 from "https://questions-statements-api.parliament.uk/index.html"
    if response.status_code == 200:

        #Parse the JSON response into a Python dictionary
        data = response.json()

        #Append the data to the results list
        results.append(data)

    elif response.status_code == 404:
        #Append the error message to the errors list
        errors_404 = SKIP

        print(f"Error fetching data for ID as it is not found{SKIP}")
        # Optionally, sleep for longer if an error occurs to give the server a break
        # As far as I know, the server does not have a rate limit
        time.sleep(1)
    
    elif response.status_code == 500:
        errors_500 = SKIP

        print(f"Error fetching data for ID due to server error{SKIP}")
    
    elif response.status_code == 400:
        errors_400 = SKIP

        print(f"Error fetching data for ID due to bad request{SKIP}")

    return results, errors_404, errors_500, errors_400

#There is not limit for UK Parliament API for now, we can skip settiing the API key or the Entry per request
#ENTRIES_PER_REQUEST = 250
#API_KEY = get_key(int(sys.argv[2]))


#There is no argument to pass to the document   
# PATH = (str(sys.argv[1]))
# MEM_ID_START = int(sys.argv[2])
# MEM_ID_END = int(sys.argv[3])
# QA_ID_START = 346849
# QA_ID_END =346850




# Get the data and normalize the json file
final = []
final_noqa = []
final_404 = []
final_500 = []
final_400 = []

#Let us get the total number of results first
qa, errors_404, errors_500, errors_400 = get(SKIP = 0)
data = qa[0]
total_results = data.get('totalResults')
print(total_results)


for n in range(0, total_results, 20):
    qa, errors_404, errors_500, errors_400 = get(SKIP = n)
    if qa is not None:
        df_all = pd.json_normalize(qa,
                                record_path=['results'])
        
        if df_all.size== 0:
            final_noqa.append(n) 
        else:
            df_all.insert(0, "writtenQAID", n)
        final.append(df_all)

    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)
    if errors_400 != 0:
        final_400.append(errors_400)

#Concatenate all the lists into one dataframe
final_df = pd.concat(final, ignore_index=True)



#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_df_400 = pd.DataFrame(final_400)
final_noqa = pd.DataFrame(final_noqa)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["writtenQAID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["writtenQAID"]
if len(final_df_400) != 0:
    final_df_400.columns = ["writtenQAID"]
if len(final_noqa) != 0:
    final_noqa.columns = ["writtenQAID"]



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

    # Upload the buffer content to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True



bucket_name = 'myukdata'
folder_path = 'WrittenQA'
file_names = ['WrittenQA.csv','WrittenQA404.csv','WrittenQA500.csv', 'WrittenQA400.csv', 'WrittenQA_NoQA.csv']  # Replace with your desired S3 object names
# Create full object names with folder path
object_names = [f"{folder_path}/{file_name}" for file_name in file_names]

# Example DataFrames
dfs = [final_df, final_df_404, final_df_500, final_df_400, final_noqa]  # Replace with your actual DataFrames


# Loop over DataFrames and upload each
for df, object_name in zip(dfs, object_names):
    upload_success = upload_df_to_s3(df, bucket_name, object_name)
    if upload_success:
        print(f"Uploaded {object_name} to {bucket_name}")
    else:
        print(f"Failed to upload {object_name}")




#Store the 2 error lists in a csv file
final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/WrittenQA/WrittenQA404.csv", index=False)
final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/WrittenQA/WrittenQA500.csv", index=False)
final_df_400.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/WrittenQA/WrittenQA400.csv", index=False)
final_noqa.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/WrittenQA/WrittenQA_NoQA.csv", index=False)
# final_df_404.to_csv(f"/Users/conny/Desktop/Trial/WrittenQA404.csv", index=False)
# final_df_500.to_csv(f"/Users/conny/Desktop/Trial/WrittenQA500.csv", index=False)
# final_df_400.to_csv(f"/Users/conny/Desktop/Trial/WrittenQA400.csv", index=False)
# final_noqa.to_csv(f"/Users/conny/Desktop/Trial/WrittenQA_NoQA.csv", index=False)

final_df.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/WrittenQA/WrittenQA.csv", index=False)
# final_df.to_csv(f"/Users/conny/Desktop/Trial/WrittenQA.csv", index=False)