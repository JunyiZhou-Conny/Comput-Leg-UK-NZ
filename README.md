# UK Parliament Data Cleaning
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview-of-the-project">Overview of the Project</a></li>
    <li><a href="#qtmcluster-anaconda-scraper-envir">QTMCluster Anaconda Scraper Envir</a></li>
    <li><a href="#scraping">Scraping</a>
    <ul>
        <li><a href="#overview-of-client-server-system">Overview of Client Server System</a></li>
        <li><a href="#using-insomnia-to-bypass-cloudflare">Using Insomnia to bypass Cloudflare</a></li>
        <li><a href="#selenium">Selenium</a></li>
    </ul>
    </li>
    <li><a href="#ec2-setup">EC2 Setup</a></li>
    <li><a href="#s3-bucket-upload-and-download">S3 Bucket Upload and Download</a></li>
    <ul>
        <li><a href="#upload">Upload</a></li>
        <li><a href="#download">Download</a></li>
    </ul>   
    <li><a href="#bills">Bills</a></li>
    <ul>
        <li><a href="#billsallstages">BillsAllStages</a></li>
        <li><a href="#billslateststage_date">BillsLatestStage_Date</a></li>
        <li><a href="#billslateststage_id">BillsLatestStage_ID</a></li>
    </ul>
    <li><a href="#members">Members</a>
    <ul>
        <li><a href="#members">Members</a></li>
        <li><a href="#members-biogrphy">Member Biography</a></li>
        <li><a href="#members-experience">Member Experience</a></li>
    </ul>
    </li>
    <li><a href="#amendment">Amendment</a></li>
    <li><a href="#publication">Publication</a></li>
    <li><a href="#common-division">Common Division</a>
    <ul>
        <li><a href="#commondivisionayetellers">CommonDivisionAyeTellers</a></li>
        <li><a href="#commondivisionntellers">CommonDivisionNoTellers</a></li>
        <li><a href="#division-per-member">Division Per Member</a></li>
    </ul>
    </li>
    <li><a href="#writtenqa">WrittenQA</a></li>
    <li><a href="#oral-questions">Oral Questions</a></li>
  </ol>
</details>

## Overview of the Project
In the UK Parliament, the legislative processes and instruments are somewhat different from those in the US Congress. The primary instruments are "Bills" and various types of "Motions." Unlike the US Congress, the UK Parliament does not use the term "resolution" in the same way, but motions serve a similar purpose. Here's a breakdown:

### Bills in UK Parliament
Purpose: A Bill is a proposal for new legislation or an amendment to existing legislation. Once a Bill has been debated and, if approved, has passed through all its parliamentary stages in both Houses of Parliament, it is sent to the reigning monarch for Royal Assent. Once Royal Assent is given, a Bill becomes an Act of Parliament and is law.

Types: There are several types of Bills – Public Bills, Private Bills, Hybrid Bills, and Private Members' Bills. Public Bills are the most common and usually involve government policy.

Process: The process includes several stages – First Reading, Second Reading, Committee Stage, Report Stage, Third Reading, followed by the same process in the other House, and finally, Royal Assent.

### Motions in UK Parliament
Purpose: Motions are formal statements put before a House for debate and possibly a decision. They are the usual method by which Members of Parliament or Lords can formally express their opinions or make decisions.

Types:
1. Early Day Motions (EDMs): Used in the House of Commons for MPs to draw attention to specific events or campaigns. They are rarely debated.
2. Substantive Motions: Can be debated and voted on. They often relate to government policy.
3. Procedural Motions: Relate to the business of the House or its Committees.
Impact: While motions can express the will of a House, they do not have the same legislative impact as a Bill. They are often used to express opinions or make specific requests of the government but do not create law.

### Key Differences from the US
The UK system does not use "resolutions" in the same way as the US. Instead, various types of motions are used to express opinions or make procedural decisions.
The role of the monarchy in the UK legislative process is largely ceremonial today, but Royal Assent is still a formal requirement for a Bill to become law.
The UK Parliament's legislative process is characterized by its parliamentary sovereignty, meaning it can make or unmake any law, and no other body can overturn its legislation.

## QTMCluster Anaconda Scraper Envir
![conda scraper.png](https://github.com/JunyiZhou-Conny/Comput-Leg-UK/blob/main/Images/hansardinspect.png)
## Scraping
### Overview of Client-Server System
SSL stands for Secure Socket Layer
TSL stands for Transport Secure Layer
Browser tries to connect with the server. Client messages server to initiate SSL/TLS communication.
Server sends back an encrypted public key/certificate
Clients check the certificate, creates and send an encrypted key back to the server
Server decrypts the key and delivers encrypted content with key to the client
Client decrypts the content, thus completing the SSL/TLS handshake

### Using Insomnia to bypass Cloudflare
Cloudflare response comparison:  
Example 1: 
Response: 403  
date: Thu, 21 Dec 2023 04:33:22 GMT  
content-type: text/html; charset=UTF-8  
cross-origin-embedder-policy: require-corp  
cross-origin-opener-policy: same-origin  
cross-origin-resource-policy: same-origin  
origin-agent-cluster: ?1  
cf-mitigated: challenge  
cache-control: private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0  
expires: Thu, 01 Jan 1970 00:00:01 GMT  
vary: Accept-Encoding  
permissions-policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), usb=()  
referrer-policy: strict-origin  
strict-transport-security: max-age=2592000  
x-content-type-options: nosniff  
x-frame-options: SAMEORIGIN  
x-xss-protection: 1; mode=block  
server: cloudflare  
cf-ray: 838d6811f9f753d5-ATL  
content-encoding: br  
alt-svc: h3=":443"; ma=86400  

Analysis:  
1 thing to notice:  
cf-mitigated: challenge suggests that Cloudflare presented a challenge.

Example 2:  
Response code: 403  
date: Thu, 21 Dec 2023 04:36:23 GMT  
content-type: text/html; charset=UTF-8  
cross-origin-embedder-policy: require-corp  
cross-origin-opener-policy: same-origin  
cross-origin-resource-policy: same-origin  
origin-agent-cluster: ?1  
cf-mitigated: challenge  
cache-control: private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0  
expires: Thu, 01 Jan 1970 00:00:01 GMT  
set-cookie:  __cf_bm=FkTyI5EdbhHPnsQDg2LXrmziuS4nLh44tFcLhbfxk10-1703133383-1-Ab4gmFj600wroVlUZ3Rluxk0cV3c0d5KvMvDMrwbRDyyazBtQidbJ4djkRZBwzXOD5KQ6v3RJudmpelPzNDf7Mg=; path=/; expires=Thu, 21-Dec-23 05:06:23 GMT; domain=.parliament.uk; HttpOnly; Secure; SameSite=None
vary: Accept-Encoding
permissions-policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), usb=()  
referrer-policy: strict-origin  
strict-transport-security: max-age=2592000  
x-content-type-options: nosniff  
x-frame-options: SAMEORIGIN  
x-xss-protection: 1; mode=block  
server: cloudflare  
cf-ray: 838d6c80ecc9673e-ATL  
content-encoding: br  
alt-svc: h3=":443"; ma=86400  

Analysis:
There are 2 things to notice:
1. cf-mitigated: challenge suggests that Cloudflare presented a challenge.
2. set-cookie: __cf_bm=FkTyI5EdbhHPnsQDg2LXrmziuS4nLh44tFcLhbfxk10-1703133383-1-Ab4gmFj600wroVlUZ3Rluxk0cV3c0d5KvMvDMrwbRDyyazBtQidbJ4djkRZBwzXOD5KQ6v3RJudmpelPzNDf7Mg=; path=/; expires=Thu, 21-Dec-23 05:06:23 GMT; domain=.parliament.uk; HttpOnly; Secure; SameSite=None suggests that Cloudflare set a cookie.
This suggests that I have passes the Cloudflare challenge. However, I am still getting a 403 error.
Basically, I am stuck here as I do not know how to incorporate this new cookie to my request. 

### Selenium
Selenium is a web developer tool that is used to test the operations of a website. However, I am using this to pypass cloudflare. The main idea of Selenium to initiate a web browswer and let selenium click the front end interface. You will see the web browser opening and loading the content much like how a human being would interact with the web browser. This is similar to MAA, which, if you are familiar with Arknights, is a tool to complete daily tasks in a way as if a robot is sitting right in front of the desktop and clicking buttons for you. 

To accomplish this, here are a few basic steps:
1. You need to download a webdriver. As the name suggests, webdriver drives a browser natively, as a user would, either locally or on a remote machine using the Selenium server. We need to make sure that the web driver installed as appropriate to our browser version.

2. I am using Chrome, and a recent update allows this matching step to be simplified. Previously, in order to test the web, the developer needs to make sure that the webdriver corresponds with the correct version of the web browswer. However, currently, with the webdriver-manager and chromedriver, this can be done automatically. Plus, if you want to test your web on on older version, it could roll back and downgrade your browswer automatically for you. I will talk about it in a later section.

#### ChromeDriver and Webdriver_Manager
ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome. It is maintained by the Chromium team with help from WebDriver contributors. 
Webdriver_Manager is a library that helps to download and install the latest version of the web drivers automatically.
'''python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
'''

Here is one example where I went onto a login page and input the correct credentials. In particular, notice that I am compying the xPath of the text box and then send the credential over.
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'http://the-internet.herokuapp.com/login'
driver.get(url)

# Using the new find_element method with By.XPATH
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys('tomsmith')
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('SuperSecretPassword!')
driver.find_element(By.XPATH, '//*[@id="login"]/button').click()
```




## EC2 Setup
This guide outlines the steps to set up JupyterLab on an AWS EC2 instance, configure the security group, and access JupyterLab remotely.

### Step 1: Configure the Security Group

- **Login to AWS Management Console.**
- **Navigate to EC2 dashboard.**
- **Select your EC2 instance's security group.**
- **Edit inbound rules:**
  - Add SSH rule: 
    - Type: SSH
    - Port Range: 22
    - Source: Your IP or Anywhere
  - Add JupyterLab rule: 
    - Type: Custom TCP
    - Port Range: 8888
    - Source: Your IP or Anywhere

### Step 2: Connect to the EC2 Instance via SSH

Use the following command to SSH into your instance:

```bash
ssh -i /path/to/your-key.pem ec2-user@your-instance-public-dns
```

### Step 3: Install JupyterLab in a Virtual Environment
```bash
sudo yum update -y # Update the package manager
sudo yum install python3-pip python3-dev -y # Install pip and python3
python3 -m venv myenv # Create a virtual environment
source myenv/bin/activate # Activate the virtual environment
pip install jupyterlab # Install JupyterLab
```

### Step 4: Start JupyterLab Manually
```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

### Step 5: Set Up JupyterLab as a Systemed Service
Create a systemd service file for JupyterLab:
```bash
sudo nano /etc/systemd/system/jupyter.service
```

Write the following into the file:
```ini
[Unit]
Description=Jupyter Lab

[Service]
Type=simple
PIDFile=/run/jupyter.pid
ExecStart=/bin/bash -c 'source /home/ec2-user/myenv/bin/activate && exec /home/ec2-user/myenv/bin/jupyter lab --ip=0.0.0.0 --port=8888 --no-browser'
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable jupyter
sudo systemctl start jupyter
```
### Use token to access JupyterLab
```bash
jupyter server list
```
And then use the token to access JupyterLab from your browser.

## S3 Bucket Upload and Download
### Upload
There are 2 scenarios for uploading files to S3:
1. Upload a file to S3 from a local file system
2. Upload a file to S3 using IAM credentials such as an EC2 instance
The key difference is that you need to set up credentials locally for the first scenario. The credentials need to be stored in a file called `~/.aws/credentials` in the following format:
You can use nano to create the file:
```bash
nano ~/.aws/credentials
```
And then paste the following into the file:
```bash
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```


where "default" is the name of the profile. It is important to pass the `profile_name` argument to the `Session` object when using the `boto3` library. Otherwise, the default profile will be used. The second case is simpler because IAM credentials are automatically retrieved from the instance metadata. No need for the use of `Session` object.
```python
import boto3
import io
bucket_name = 'myukdata'
folder_path = 'Member'
file_names = ['Member.csv','Member_404.csv','Member_500.csv']  # Replace with your desired S3 object names
# Create full object names with folder path
object_names = [f"{folder_path}/{file_name}" for file_name in file_names]

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
```

### Download
The download function is similar to the upload function. The key difference is that the `download_file` method is used instead of the `put_object` method. The `download_file` method takes 3 arguments: the bucket name, the object name, and the local file name.
```python
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
```

## Bills
### BillsAllStages
Everything is about automation. We want to automate the process of data collection. To this end, we need to figure out a way so that we can allocate the last bill ID so that the python script can run a for loop to collect all the bills.

In this case, using the given API, there is no direct access to the last bill ID. To work around this, we can use the following code to get the last bill ID. 

```python
#Get the total number of results from a different source
url = f'https://bills-api.parliament.uk/api/v1/Bills?CurrentHouse=All&OriginatingHouse=All'
response = requests.get(url)
total_results = response.json()['totalResults']

iter = 0
n = 0
while iter < total_results:
    bills, errors_404, errors_500, errors_400 = get(BillID = n)
    
    if bills is not None:
        df_all = pd.json_normalize(bills,
                                   record_path =['items'])
        #Add the BillID column to the very left of the dataframe
        df_all.insert(0, 'BillID', n)
        final.append(df_all)
        iter += 1
    #Write a if statement to check if bills is a list with an empty list inside
    if pd.json_normalize(bills, record_path =['items']) is None:
        final_nobill.append(n)
    if errors_404 != 0:
        final_404.append(errors_404)
    if errors_500 != 0:
        final_500.append(errors_500)
    if errors_400 != 0:
        final_400.append(errors_400)
    n += 1
print(n)
```
We use 2 indicators. "iter" makes sure that the while loop stops when it reaches the total number of results. "n" is the bill ID. We start with n = 0 and increase it by 1 each time the while loop runs.

Also it is worth noting how we define final_nobill. From observation, I have not yet found a special case where the requested bill has the following json structure.
    
    ```json
    {'items': [], 
    'totalResults': 48, 
    'itemsPerPage': 100}
    ```

Here, we are making the assumption that the json file contains a key called "items" and the value of this key is a list with an empty list inside. If this is the case, we append the bill ID to the final_nobill list. We can check this with the following code.

```python
if pd.json_normalize(bills, record_path =['items']) is None:
        final_nobill.append(n)
```

### BillsLatestStage_Date
BillsLatestStage is gathered using the date parameter. It retrieves back all the bills that have been updated since the date specified. The date is set to be 2050-01-01. The issue is that the API contains limited information.

So, I am thinking about repeating the whole process using the method specified in BillsAllStages. The only difference is that we are going to use the date parameter instead of the BillID parameter.

### BillsLatestStage_ID
The worst part of retriving data using the BillID parameter is that the sponsor of the bill is in a nested dictionary. This makes it very hard to retrieve the sponsor information. But I made it.

Notice that sponsors_dict capture the memberId. We do not need the rest of the information because we can refer to Member dataset.

Also, be aware that we need to change the logic of the elif statement to make sure that it will skip the json_normalize function if the json file is 404.

Another interesting thing(not sure why I said interesting), start the BillID from 1 instead of 0, otherwise the screen will shiver to tell you that the API is not working.

There are a lot of edge cases. The memberId may not exist for every bill. So we need to use try and except to catch the error. Also there are missing columns, so we set up a desired column list to select the actual columns we have from.
```python
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
```

## Members
### Members
### Members Biography
### Members Experience

## Amendment

## Publication

## Common Division
### CommonDivisionAyeTellers
### CommonDivisionNoTellers
### Division Per Member

## WrittenQA

## Oral Questions
This is the very first attempt during this research project to use some web scraping techniques. The goal is to find the url of each oral question. To clarify the purpose, let us take a concrete example, "https://hansard.parliament.uk/commons/2023-12-19/debates/613A8188-0B79-4319-A56F-757942540B71/OralAnswersToQuestions". This is the url fo the oral answers to questions. As you can see, it consists of the date, the standard hansard header. However, there is a unique identifier for each oral question, which is "613A8188-0B79-4319-A56F-757942540B71". This is the unique identifier that we are looking for.

To consistently find the unique identifier, what we do is that we go to the following webpage:
"https://hansard.parliament.uk/commons/2023-12-19". This is a very standard hansard webpage that contains information regarding everything happened on that day. 

![hansardinspect.png](https://github.com/JunyiZhou-Conny/Comput-Leg-UK/blob/main/Images/hansardinspect.png)

```python
from curl_cffi import requests
from bs4 import BeautifulSoup
```
There are the 2 major libraries that we need to use. curl_cffi is a library that can bypass the Cloudflare protection. BeautifulSoup is a library that can help us to parse the html file.

For each date in the generated range:
1. Retrieve URLs for oral answers.
2. If no URLs are found, log the date.
3. Otherwise, download the text for the first URL.
4. If text is available, it's converted to a DataFrame and uploaded to an S3 bucket.
5. Two lists, OralQuestions_NoOral and OralQuestions_NoText, are used to keep track of dates where no oral questions or no texts were found, respectively. These lists are converted to DataFrames and uploaded to the S3 bucket.

Key Points to Note:
1. Error Handling: The script has robust error handling for HTTP requests and AWS operations.
AWS Credentials: The script is set up to handle AWS credentials both locally and through IAM roles, which is crucial for security and flexibility in different environments.
2. Impersonation: The script uses the impersonate='chrome110' argument in requests. This might be part of the custom curl_cffi package to mimic a particular browser's behavior.
```python
session = requests.Session()
response = session.get(url, impersonate='chrome110')
```
3. Data Upload: The script doesn't just scrape data but also processes and uploads it in a structured format (CSV) to AWS S3.
4. Date Handling: The script uses Python's datetime library to iterate over a range of dates, which is a common approach in data scraping tasks that are date-based.


### I do not know what is wrong with the data in 2018/10/22, my preliminary investigation shows me that the cause of parsing problem originates from line 324 in the original text where the data includes a Chinese double quotation mark for some reasons. 












## Roadmap
- [x] bill stage identifier automation
- [x] bill type identifier automation
- [x] constituency automation
- [x] committee automation
- [x] member folders have 3 missing bash files
- [x] modify billslateststage
- [x] combine billslatestage using date and billslateststage using id together





## Authors

Contributors names and contact info

Name: Dr. Juan Estrada
Contact:

Name: Junyi (Conny) Zhou  
Contact: junyi.zhou@emory.edu




## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
