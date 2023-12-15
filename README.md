# UK Parliament Data Cleaning
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#ec2-setup">EC2 Setup</a></li>
    <li><a href="#bills">Bills</a></li>
    <ul>
        <li><a href="#billsallstages">BillsAllStages</a></li>
        <li><a href="#billslateststage_date">BillsLatestStage_Date</a></li>
        <li><a href="#billslateststage_id">BillsLatestStage_ID</a></li>
    <li><a href="#members">Members</a></li>
    <li><a href="#data-preprocessing">Data Preprocessing</a></li>
    <li><a href="#description-of-the-processed-dataset">Description of the Processed Dataset</a></li>
    <li><a href="#modeling">Modeling</a></li>
    <ul>
        <li><a href="#knn">KNN</a></li>
        <li><a href="#principal-component-regression">Principal Component Regression</a></li>
    <li><a href="#random-forest">Random Forest</a></li>
    <li><a href="#convolutional-neural-network">Convolutional Neural Network</a></li>
      </ul>
  </ol>
</details>

## Overview of the Project
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
sudo yum update -y
sudo yum install python3-pip python3-dev -y
python3 -m venv myenv
source myenv/bin/activate
pip install jupyterlab
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
        #Extract the member ID from the sponsors list
        sponsors_dict = pd.json_normalize(bills,
                                   record_path=['sponsors'],
                                   meta=['billId'])[['member.memberId','billId']]
        almost_all = pd.json_normalize(bills)[['longTitle', 
                                         'summary', 
                                         'petitioningPeriod',
                                         'petitionInformation',
                                         'agent',
                                         'shortTitle',
                                         'currentHouse',
                                         'originatingHouse',
                                         'lastUpdate',
                                         'billWithdrawn',
                                         'isDefeated',
                                         'billTypeId',
                                            'introducedSessionId',
                                            'includedSessionIds',
                                            'isAct',
                                            'currentStage.id',
                                            'currentStage.sessionId',
                                            'currentStage.description',
                                            'currentStage.abbreviation',
                                            'currentStage.house',
                                            'currentStage.stageSittings',
                                            'currentStage.sortOrder']]
        df_all = pd.concat([sponsors_dict, almost_all], axis=1)                          
        #Add the BillID column to the very left of the dataframe
        final.append(df_all)
        iter += 1
    #Write a if statement to check if bills is a list with an empty list inside
    
    n += 1
print(n)
```













## Roadmap
12/9/2023
- [] bill stage identifier automation
- [] bill type identifier automation
- [] constituency automation
- [] committee automation
- [x] member folders have 3 missing bash files
- [x] modify billslateststage
- [] combine billslatestage using date and billslateststage using id together





## Authors

Contributors names and contact info

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
