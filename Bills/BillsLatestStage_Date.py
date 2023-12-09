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


    url = f"https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedAscending&Skip={SKIP}&Take=20"
    response = requests.get(url)

    #Currently, the success code is 200 from "https://bills-api.parliament.uk/index.html"
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


# PATH = (str(sys.argv[1]))
# MEM_ID_START = int(sys.argv[2])
# MEM_ID_END = int(sys.argv[3])



# Get the data and normalize the json file
final = []
final_nobill = []
final_404 = []
final_500 = []
final_400 = []

#Let us get the total number of results first
bills, errors_404, errors_500, errors_400 = get(SKIP = 0)
data = bills[0]
total_results = data['totalResults']
print(total_results)

for n in range(0, total_results, 20):
    bills, errors_404, errors_500, errors_400 = get(SKIP = n)
    if bills is not None:
        df_all = pd.json_normalize(bills,
                                   record_path =['items'])
        #df_all = df_all.replace(r'\n', ' ', regex=True)
        #df_all = df_all.replace(r'\r', ' ', regex=True)
        #df_all = df_all.replace(r'\t', ' ', regex=True)
        final.append(df_all)
    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)
    if errors_400 != 0:
        final_400.append(errors_400)
    if pd.json_normalize(bills, record_path =['items']) is None:
        final_nobill.append(n)

#Concatenate all the lists into one dataframe
final_df = pd.concat(final, ignore_index=True)
final_df.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Bills/BillsLatestStage_Date/BillsLatestStage_Date.csv", index=False)
# final_df.to_csv(f"/Users/conny/Desktop/Trial/BillsLatestStage_Date.csv", index=False)

#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_df_400 = pd.DataFrame(final_400)
final_df_nobill = pd.DataFrame(final_nobill)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["SKIP"]
if len(final_df_500) != 0:
    final_df_500.columns = ["SKIP"]
if len(final_df_400) != 0:
    final_df_400.columns = ["SKIP"]
if len(final_df_nobill) != 0:
    final_df_nobill.columns = ["SKIP"]

#Store the 2 error lists in a csv file
final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Bills/BillsLatestStage_Date/BillsLatestStage_Date404.csv", index=False)
final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Bills/BillsLatestStage_Date/BillsLatestStage_Date500.csv", index=False)
final_df_400.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Bills/BillsLatestStage_Date/BillsLatestStage_Date400.csv", index=False)
final_df_nobill.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Bills/BillsLatestStage_Date/BillsLatestStage_DateNoBill.csv", index=False)
# final_df_404.to_csv(f"/Users/conny/Desktop/Trial/BillsLatestStage_Date404.csv", index=False)
# final_df_500.to_csv(f"/Users/conny/Desktop/Trial/BillsLatestStage_Date500.csv", index=False)
# final_df_400.to_csv(f"/Users/conny/Desktop/Trial/BillsLatestStage_Date400.csv", index=False)
# final_df_nobill.to_csv(f"/Users/conny/Desktop/Trial/BillsLatestStage_DateNoBill.csv", index=False)


