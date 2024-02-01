'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 11/29/2023
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


    url = f"https://commonsvotes-api.parliament.uk/data/divisions.json/search?queryParameters.skip={SKIP}&queryParameters.take=20&queryParameters.endDate=2050-01-01"
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
        time.sleep(5)
    
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





# Get the data and normalize the json file
final = []
final_nocd = []
final_404 = []
final_500 = []
final_400 = []

#Let us get the last common division ID
url = f"https://commonsvotes-api.parliament.uk/data/divisions.json/search?queryParameters.skip=0&queryParameters.take=1&queryParameters.endDate=2050-01-01"
response = requests.get(url)
data = response.json()
lasat_cdID = data[0]['DivisionId']
print(lasat_cdID)


for n in range(0, lasat_cdID, 20):
    cd, errors_404, errors_500, errors_400 = get(SKIP=n)
    if cd is not None:
        # df_all = pd.json_normalize(cd,
        #                         record_path=['Ayes'],
        #                         meta=['Date',
        #                         'Number',
        #                         'IsDeferred',
        #                         'EVELType',
        #                         'EVELCountry',
        #                         'Title',
        #                         'AyeCount',
        #                         'NoCount',
        #                         'DoubleMajorityAyeCount',
        #                         'DoubleMajorityNoCount'])
        df_all = pd.json_normalize(cd)

        #for each column in df_all, it is an object, a list of dictionaries,we want to normalize it
        df_all.insert(0, "commonDivisionID", n)

        print(f"Skip {n} has {df_all.shape[1]} columns")
        for i in range(df_all.shape[1] - 1):  
            temp = pd.json_normalize(df_all[i],
            meta=['DivisionId', 
                    'Date',
                    'Number',
                    'IsDeferred',
                    'EVELType',
                    'EVELCountry',
                    'Title',
                    'AyeCount',
                    'NoCount',
                    'DoubleMajorityAyeCount',
                    'DoubleMajorityNoCount'],
                record_path=['AyeTellers'])
            final.append(temp)

    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)
    if errors_400 != 0:
        final_400.append(errors_400)

#Concatenate all the lists into one dataframe
for df in final:
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() == 2 and set(df[col].unique()) == {True, False}:
            df[col] = df[col].astype(bool)

final_df = pd.concat(final, ignore_index=True)

final_df.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/CommonDivision/CommonDivisionAyeTellers/CommonDivisionAyeTellers.csv", index=False)
#final_df.to_csv(f"/Users/conny/Desktop/Trial/CommonDivisionAyeTellers.csv", index=False)


#Transfrom the error lists into dataframes
final_df_404 = pd.DataFrame(final_404)
final_df_500 = pd.DataFrame(final_500)
final_df_400 = pd.DataFrame(final_400)
final_nocd = pd.DataFrame(final_nocd)

#Make the column name of the error lists as "ID"
if len(final_df_404) != 0:
    final_df_404.columns = ["commonDivisionID"]
if len(final_df_500) != 0:
    final_df_500.columns = ["commonDivisionID"]
if len(final_df_400) != 0:
    final_df_400.columns = ["commonDivisionID"]
if len(final_nocd) != 0:
    final_nocd.columns = ["commonDivisionID"]


#Store the 2 error lists in a csv file
final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/CommonDivision/CommonDivisionAyeTellers/CommonDivisionAyeTellers404.csv", index=False)
final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/CommonDivision/CommonDivisionAyeTellers/CommonDivisionAyeTellers500.csv", index=False)
final_df_400.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/CommonDivision/CommonDivisionAyeTellers/CommonDivisionAyeTellers400.csv", index=False)
final_nocd.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/CommonDivision/CommonDivisionAyeTellers/CommonDivisionAyeTellers_NoCD.csv", index=False)
# final_df_404.to_csv(f"/Users/conny/Desktop/Trial/CommonDivisionAyeTellers404.csv", index=False)
# final_df_500.to_csv(f"/Users/conny/Desktop/Trial/CommonDivisionAyeTellers500.csv", index=False)
# final_df_400.to_csv(f"/Users/conny/Desktop/Trial/CommonDivisionAyeTellers400.csv", index=False)
# final_nocd.to_csv(f"/Users/conny/Desktop/Trial/CommonDivisionAyeTellers_NoCD.csv", index=False)








