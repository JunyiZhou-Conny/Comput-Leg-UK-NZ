'''
Author: Conny Zhou
Email: junyi.zhou@emory.edu
Last Updated: 12/15/2023
'''

import boto3
import pandas as pd

def download_file_from_s3(bucket, object_name, local_file_name):
    """
    Download a file from S3 to the local file system.

    :param bucket: Name of the S3 bucket
    :param object_name: S3 object name
    :param local_file_name: Local file name to save the downloaded file
    """
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket, object_name, local_file_name)

bucket_name = 'your-bucket-name'
s3_file_names = ['folder_name/file1.csv', 'folder_name/file2.csv']
local_file_names = ['local_file1.csv', 'local_file2.csv']

# Download files
for s3_file, local_file in zip(s3_file_names, local_file_names):
    download_file_from_s3(bucket_name, s3_file, local_file)

# Read into pandas DataFrames
df1 = pd.read_csv(local_file_names[0])
df2 = pd.read_csv(local_file_names[1])

# Now df1 and df2 hold your data for analysis
