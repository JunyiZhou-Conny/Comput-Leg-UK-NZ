'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 11/19/2023
'''
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


    url = f"https://members-api.parliament.uk/api/Members/{MEM_ID}/Experience"
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


PATH = (str(sys.argv[1]))
MEM_ID_START = int(sys.argv[2])
MEM_ID_END = int(sys.argv[3])
# MEM_ID_START = 2000
# MEM_ID_END =2001




# Get the data and normalize the json file
final = []
final_noexp = []
final_404 = []
final_500 = []

for ID in range(MEM_ID_START, MEM_ID_END + 1):
    member, errors_404, errors_500 = get(MEM_ID = ID)

    if member is not None:
        df_all = pd.json_normalize(member,
                                   record_path = ['value'])
        #Deal wit the case that there is no experience for a member
        if df_all.size== 0:
            final_noexp.append(ID) 
        else:
            df_all.insert(0, "memberID", ID)
        final.append(df_all)

    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)

#Concatenate all the lists into one dataframe
final_df = pd.concat(final, ignore_index=True)
final_df.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Experience.csv", index=False)
#final_df.to_csv(f"/Users/conny/Desktop/Member_Experience.csv", index=False)


#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_noexp = pd.DataFrame(final_noexp)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["memberID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["memberID"]
if len(final_noexp) != 0:
    final_noexp.columns = ["memberID"]


#Store the 2 error lists in a csv file
final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Exp404.csv", index=False)
final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Exp500.csv", index=False)
final_noexp.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_NoExp.csv", index=False)
# final_df_404.to_csv(f"/Users/conny/Desktop/Member_Exp404.csv", index=False)
# final_df_500.to_csv(f"/Users/conny/Desktop/Member_Exp500.csv", index=False)
# final_noexp.to_csv(f"/Users/conny/Desktop/Member_NoExp.csv", index=False)

