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


    url = f"https://members-api.parliament.uk/api/Members/{MEM_ID}/Biography"
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
# MEM_ID_START =  2000
# MEM_ID_END = 2000

# Get the data and normalize the json file
representations = pd.DataFrame()
final_representations = pd.DataFrame()
final_norepresentations = []

electionsContested =pd.DataFrame()
final_electionsContested = pd.DataFrame()
final_noelectionsContested = []

houseMemberships = pd.DataFrame()
final_houseMemberships = pd.DataFrame()
final_nohouseMemberships = []

governmentPosts = pd.DataFrame()
final_governmentPosts = pd.DataFrame()
final_nogovernmentPosts = []

oppositionPosts = pd.DataFrame()
final_oppositionPosts = pd.DataFrame()
final_nooppositionPosts = []

otherPosts = pd.DataFrame()
final_otherPosts = pd.DataFrame()
final_nootherPosts = []

partyAffiliations = pd.DataFrame()
final_partyAffiliations = pd.DataFrame()
final_nopartyAffiliations = []

committeeMemberships = pd.DataFrame()
final_committeeMemberships = pd.DataFrame()
final_nocommitteeMemberships = []

final_404 = []
final_500 = []

for ID in range(MEM_ID_START, MEM_ID_END + 1):
    member, errors_404, errors_500 = get(MEM_ID = ID)

# I decide to separate the data into different lists based on the type of data
    if member is not None:
        df_representations = pd.json_normalize(member, record_path=['value', 'representations'])
        if df_representations.size == 0:
            final_norepresentations.append(ID)
        else:
            new_column_data = [ID] * len(df_representations)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            representations = pd.concat([memberID, df_representations], axis = 1)
            final_representations = pd.concat([final_representations, representations], axis = 0, ignore_index=True)


        df_electionsContested = pd.json_normalize(member, record_path=['value', 'electionsContested'])
        if df_electionsContested.size == 0:
            final_noelectionsContested.append(ID)
        else:
            new_column_data = [ID] * len(df_electionsContested)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            electionsContested = pd.concat([memberID, df_electionsContested], axis = 1)
            final_electionsContested = pd.concat([final_electionsContested, electionsContested], axis = 0, ignore_index=True)
        
        df_houseMemberships = pd.json_normalize(member, record_path=['value', 'houseMemberships'])
        if df_houseMemberships.size == 0:
            final_nohouseMemberships.append(ID)
        else:
            new_column_data = [ID] * len(df_houseMemberships)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            houseMemberships = pd.concat([memberID, df_houseMemberships], axis = 1)
            final_houseMemberships = pd.concat([final_houseMemberships, houseMemberships], axis = 0, ignore_index=True)

        df_governmentPosts = pd.json_normalize(member, record_path=['value', 'governmentPosts'])
        if df_governmentPosts.size == 0:
            final_nogovernmentPosts.append(ID)
        else:
            new_column_data = [ID] * len(df_governmentPosts)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            governmentPosts = pd.concat([memberID, df_governmentPosts], axis = 1)
            final_governmentPosts = pd.concat([final_governmentPosts, governmentPosts], axis = 0, ignore_index=True)

        df_oppositionPosts = pd.json_normalize(member, record_path=['value', 'oppositionPosts'])
        if df_oppositionPosts.size == 0:
            final_nooppositionPosts.append(ID)
        else:
            new_column_data = [ID] * len(df_oppositionPosts)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            oppositionPosts = pd.concat([memberID, df_oppositionPosts], axis = 1)
            final_oppositionPosts = pd.concat([final_oppositionPosts, oppositionPosts], axis = 0, ignore_index=True)
            

        df_otherPosts = pd.json_normalize(member, record_path=['value', 'otherPosts'])
        if df_otherPosts.size == 0:
            final_nootherPosts.append(ID)
        else:
            new_column_data = [ID] * len(df_otherPosts)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            otherPosts = pd.concat([memberID, df_otherPosts], axis = 1)
            final_otherPosts = pd.concat([final_otherPosts, otherPosts], axis = 0, ignore_index=True)

        df_partyAffiliations = pd.json_normalize(member, record_path=['value', 'partyAffiliations'])
        if df_partyAffiliations.size == 0:
            final_nopartyAffiliations.append(ID)
        else:
            new_column_data = [ID] * len(df_partyAffiliations)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            partyAffiliations = pd.concat([memberID, df_partyAffiliations], axis = 1)
            final_partyAffiliations = pd.concat([final_partyAffiliations, partyAffiliations], axis = 0, ignore_index=True)

        df_committeeMemberships = pd.json_normalize(member, record_path=['value', 'committeeMemberships'])
        if df_committeeMemberships.size == 0:
            final_nocommitteeMemberships.append(ID)
        else:
            new_column_data = [ID] * len(df_committeeMemberships)
            memberID = pd.DataFrame()
            memberID.insert(0,  'memberID', new_column_data)
            committeeMemberships = pd.concat([memberID, df_committeeMemberships], axis = 1)
            final_committeeMemberships = pd.concat([final_committeeMemberships, committeeMemberships], axis = 0, ignore_index=True)


    if errors_404 != 0:
        final_404.append(errors_404)

    if errors_500 != 0:
        final_500.append(errors_500)

#Concatenate the error list into a dataframe
final_norepresentations = pd.DataFrame(final_norepresentations)
final_noelectionsContested = pd.DataFrame(final_noelectionsContested)
final_nohouseMemberships = pd.DataFrame(final_nohouseMemberships)
final_nogovernmentPosts = pd.DataFrame(final_nogovernmentPosts)
final_nooppositionPosts = pd.DataFrame(final_nooppositionPosts)
final_nootherPosts = pd.DataFrame(final_nootherPosts)
final_nopartyAffiliations = pd.DataFrame(final_nopartyAffiliations)
final_nocommitteeMemberships = pd.DataFrame(final_nocommitteeMemberships)

#Make the column name of the error lists as "ID"
if len(final_norepresentations) != 0:
    final_norepresentations.columns = ['memberID']
if len(final_noelectionsContested) != 0:
    final_noelectionsContested.columns = ['memberID']
if len(final_nohouseMemberships) != 0:
    final_nohouseMemberships.columns = ['memberID']
if len(final_nogovernmentPosts) != 0:
    final_nogovernmentPosts.columns = ['memberID']
if len(final_nooppositionPosts) != 0:
    final_nooppositionPosts.columns = ['memberID']
if len(final_nootherPosts) != 0:
    final_nootherPosts.columns = ['memberID']
if len(final_nopartyAffiliations) != 0:
    final_nopartyAffiliations.columns = ['memberID']
if len(final_nocommitteeMemberships) != 0:
    final_nocommitteeMemberships.columns = ['memberID']


#Transfrom the error lists into dataframes
final_bio_404 = pd.DataFrame(final_404)
final_bio_500 = pd.DataFrame(final_500)


#Make the column name of the error lists as "ID"
if len(final_bio_404) != 0:
    final_bio_404.columns = ["memberID"]
if len(final_bio_500) != 0:
    final_bio_500.columns = ["memberID"]



final_404 = []
final_500 = []

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
folder_path = 'Member'
file_names = ['Member_Representations.csv','Member_ElectionsContested.csv','Member_HouseMemberships.csv', 
              'Member_GovernmentPosts.csv', 'Member_OppositionPosts.csv','Member_OtherPosts.csv','Member_PartyAffiliations.csv','Member_CommitteeMemberships.csv']  # Replace with your desired S3 object names
# Create full object names with folder path
object_names = [f"{folder_path}/{file_name}" for file_name in file_names]

# Example DataFrames
dfs = [final_representations, final_electionsContested, final_houseMemberships, final_governmentPosts, final_oppositionPosts,
       final_otherPosts,final_partyAffiliations,final_committeeMemberships]  # Replace with your actual DataFrames


# Loop over DataFrames and upload each
for df, object_name in zip(dfs, object_names):
    upload_success = upload_df_to_s3(df, bucket_name, object_name)
    if upload_success:
        print(f"Uploaded {object_name} to {bucket_name}")
    else:
        print(f"Failed to upload {object_name}")
























# #Save the data into QTM clustering
# final_representations.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Representations/Member_Representations.csv", index=False)
# final_electionsContested.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_ElectionsContested/Member_ElectionsContested.csv", index=False)
# final_houseMemberships.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_HouseMemberships/Member_HouseMemberships.csv", index=False)
# final_governmentPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_GovernmentPosts/Member_GovernmentPosts.csv", index=False)
# final_oppositionPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_OppositionPosts/Member_OppositionPosts.csv", index=False)
# final_otherPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_OtherPosts/Member_OtherPosts.csv", index=False)
# final_partyAffiliations.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_PartyAffiliations/Member_PartyAffiliations.csv", index=False)
# final_committeeMemberships.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_CommitteeMemberships/Member_CommitteeMemberships.csv", index=False)

#Test on my computer
# final_representations.to_csv(f"/Users/conny/Desktop/Member_Representations.csv", index=False)
# final_electionsContested.to_csv(f"/Users/conny/Desktop/Member_ElectionsContested.csv", index=False)
# final_houseMemberships.to_csv(f"/Users/conny/Desktop/Member_HouseMemberships.csv", index=False)
# final_governmentPosts.to_csv(f"/Users/conny/Desktop/Member_GovernmentPosts.csv", index=False)
# final_oppositionPosts.to_csv(f"/Users/conny/Desktop/Member_OppositionPosts.csv", index=False)
# final_otherPosts.to_csv(f"/Users/conny/Desktop/Member_OtherPosts.csv", index=False)
# final_partyAffiliations.to_csv(f"/Users/conny/Desktop/Member_PartyAffiliations.csv", index=False)
# final_committeeMemberships.to_csv(f"/Users/conny/Desktop/Member_CommitteeMemberships.csv", index=False)


# #Store the 2 error lists in a csv file
# # final_df_404.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Bio404.csv", index=False)
# # final_df_500.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Bio500.csv", index=False)
# # final_nobio.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_NoBio.csv", index=False)


# #Test on my computer
# final_bio_404.to_csv(f"/Users/conny/Desktop/Member_Bio404.csv", index=False)
# final_bio_500.to_csv(f"/Users/conny/Desktop/Member_Bio500.csv", index=False)


# #Store the empty lists in a csv file
# final_norepresentations.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_Representations/Member_RepresentationsEmpty.csv", index=False)
# final_noelectionsContested.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_ElectionsContested/Member_ElectionsContestedEmpty.csv", index=False)
# final_nohouseMemberships.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_HouseMemberships/Member_HouseMembershipsEmpty.csv", index=False)
# final_nogovernmentPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_GovernmentPosts/Member_GovernmentPostsEmpty.csv", index=False)
# final_nooppositionPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_OppositionPosts/Member_OppositionPostsEmpty.csv", index=False)
# final_nootherPosts.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_OtherPosts/Member_OtherPostsEmpty.csv", index=False)
# final_nopartyAffiliations.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_PartyAffiliations/Member_PartyAffiliationsEmpty.csv", index=False)
# final_nocommitteeMemberships.to_csv(f"/home/jjestra/research/computational_legislature/uk/Data/Member/Member_CommitteeMemberships/Member_CommitteeMembershipsEmpty.csv", index=False)

# #Test on my computer
# # final_norepresentations.to_csv(f"/Users/conny/Desktop/Member_RepresentationError.csv", index=False)
# # final_noelectionsContested.to_csv(f"/Users/conny/Desktop/Member_ElectionsContestedError.csv", index=False)
# # final_nohouseMemberships.to_csv(f"/Users/conny/Desktop/Member_HouseMembershipsError.csv", index=False)
# # final_nogovernmentPosts.to_csv(f"/Users/conny/Desktop/Member_GovernmentPostsError.csv", index=False)
# # final_nooppositionPosts.to_csv(f"/Users/conny/Desktop/Member_OppositionPostsError.csv", index=False)
# # final_nootherPosts.to_csv(f"/Users/conny/Desktop/Member_OtherPostsError.csv", index=False)
# # final_nopartyAffiliations.to_csv(f"/Users/conny/Desktop/Member_PartyAffiliationsError.csv", index=False)
# # final_nocommitteeMemberships.to_csv(f"/Users/conny/Desktop/Member_CommitteeMembershipsError.csv", index=False)