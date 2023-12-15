'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/9/2023
'''
import requests
import time
import json
import math
import sys
import pandas as pd
import io


def get(BillID):
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


    url = f"https://bills-api.parliament.uk/api/v1/Bills/{BillID}"
    response = requests.get(url)

    #Currently, the success code is 200 from "https://bills-api.parliament.uk/index.html"
    if response.status_code == 200:

        #Parse the JSON response into a Python dictionary
        data = response.json()

        #Append the data to the results list
        results.append(data)

    elif response.status_code == 404:
        #Append the error message to the errors list
        errors_404 = BillID

        print(f"Error fetching data for ID as it is not found {BillID}")
        # Optionally, sleep for longer if an error occurs to give the server a break
        # As far as I know, the server does not have a rate limit
        time.sleep(1)
    
    elif response.status_code == 500:
        errors_500 = BillID

        print(f"Error fetching data for ID due to server error {BillID}")

    elif response.status_code == 400:
        errors_400 = BillID

        print(f"Error fetching data for ID due to bad request {BillID}")

    return results, errors_404, errors_500, errors_400

#There is not limit for UK Parliament API for now, we can skip settiing the API key or the Entry per request
#ENTRIES_PER_REQUEST = 250
#API_KEY = get_key(int(sys.argv[2]))


# PATH = (str(sys.argv[1]))
# Bill_ID_START = int(sys.argv[2])
# Bill_ID_END = int(sys.argv[3])



# Get the data and normalize the json file
final = []
final_nobill = []
final_404 = []
final_500 = []
final_400 = []
final_nomemId = []

#Get the total number of results from a different source
url = f'https://bills-api.parliament.uk/api/v1/Bills?CurrentHouse=All&OriginatingHouse=All'
response = requests.get(url)
total_results = response.json()['totalResults']

iter = 0
n = 1
while iter < total_results:
    bills, errors_404, errors_500, errors_400 = get(BillID = n)
    if errors_404 != 0:
        final_404.append(errors_404)
    elif errors_500 != 0:
        final_500.append(errors_500)
    elif errors_400 != 0:
            final_400.append(errors_400)
    elif pd.json_normalize(bills) is None:
            final_nobill.append(n)
    elif bills is not None:
        try:
        # Try normalizing with member.memberId
            sponsors_dict = pd.json_normalize(bills,
                                          record_path=['sponsors'],
                                          meta=['billId'],
                                          errors='raise')[['member.memberId', 'billId']]
        except KeyError as e:
            print(f"KeyError occurred for BillId {n}: {e}")
            final_nomemId.append(n)
            # If KeyError, normalize without member.memberId
            sponsors_dict = pd.json_normalize(bills,
                                          record_path=['sponsors'],
                                          meta=['billId'],
                                          errors='ignore')
        # Add the member.memberId column with NaN values
        sponsors_dict['member.memberId'] = pd.NA
        
        df = pd.json_normalize(bills)
        # List of desired columns
        desired_columns = [
        'longTitle', 'summary', 'petitioningPeriod', 'petitionInformation', 'agent',
        'shortTitle', 'currentHouse', 'originatingHouse', 'lastUpdate',
        'billWithdrawn', 'isDefeated', 'billTypeId', 'introducedSessionId',
        'includedSessionIds', 'isAct', 'currentStage.id', 'currentStage.sessionId',
        'currentStage.description', 'currentStage.abbreviation',
        'currentStage.house', 'currentStage.stageSittings', 'currentStage.sortOrder']
                                                                        
        # Filter out the columns that don't exist in df
        existing_columns = [col for col in desired_columns if col in df.columns]

        almost_all = df[existing_columns]

        df_all = pd.concat([sponsors_dict, almost_all], axis=1)                          
        #Add the BillID column to the very left of the dataframe
        final.append(df_all)
        iter += 1
    #Write a if statement to check if bills is a list with an empty list inside
    
    n += 1
print(n)


#Concatenate all the lists into one dataframe
final_df = pd.concat(final, ignore_index=True)


#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_df_400 = pd.DataFrame(final_400)
final_df_nobill = pd.DataFrame(final_nobill)
final_nomemId = pd.DataFrame(final_nomemId)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["ID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["ID"]
if len(final_df_400) != 0:
    final_df_400.columns = ["ID"]
if len(final_df_nobill) != 0:
    final_df_nobill.columns = ["ID"]
if len(final_nomemId) != 0:
    final_nomemId.columns = ["ID"]




