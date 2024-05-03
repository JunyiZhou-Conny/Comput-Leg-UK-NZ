## Overview of Dataset

### UK: Basic Proceedings

### ![UK Proceedings.png](https://github.com/JunyiZhou-Conny/Comput-Leg-UK/blob/main/Images/UK%20Congress%20Proceedings.png)

**Q1: Where do all of the dataset currently live? How can we access them?**

**A1:** Data are stored in AWS S3 bucket. 

For those unfamiliar with S3 buckets, they're a service provided by Amazon similar to OneDrive and Google Drive. However, one standout feature of S3 buckets is their seamless integration with code. Here's how I managed the large amount of data in the UK dataset:

I relied heavily on the UK Parliament Developer Hub (https://developer.parliament.uk), which offers a range of APIs for data requests. All my data cleaning tasks were performed using Python code. After retrieving data from the Developer Hub, I utilized the boto3 library (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to directly upload the data to an S3 bucket. This approach saved both time and disk storage capacity compared to uploading to platforms like OneDrive or Google Drive.

Developers commonly refer to the AWS SDK for Python as "Boto3". It's a powerful tool for creating, configuring, and managing AWS services, including Amazon Elastic Compute Cloud (EC2) and Amazon Simple Storage Service (S3). To assist myself and future data collectors, I created a preliminary tutorial. This tutorial, available [here](https://github.com/JunyiZhou-Conny/Comput-Leg-UK?tab=readme-ov-file#s3-bucket-upload-and-download), offers guidance on conducting data cleaning through S3 buckets or EC2 instances.

It's worth noting that the dataset is organized into two main folders: Original Folder and Preprocessing Folder. The data discussed in Q2 primarily originates from the Preprocessing Folder, although I may refer back to Original Folder to provide context regarding the data's origin.

**Q2: What do we have?**

**A2:** Cleaning the UK dataset has been a thorough process, and discussing it without visual aid would be challenging. Below, I've compiled all the gathered information for clarity. To better understand the dataset's structure and relationships between its components, it would be beneficial to refer to the Entity Relationship Diagram (ER Diagram).

Here are all the data we have in the Preprocessing Folder:

1. Member:

   - Member Basic Information - Member.csv
   - Committee Membership - MemberCommitteeMemberships.csv
   - Elections Contested - MemberElectionContested.csv
   - Previous Experience - MemberExperience.csv
   - Government Posts - MemberGovernmentPosts.csv
   - House Membership - MemberHouseMemberships.csv
   - Opposition Posts - OppositionPosts.csv
   - Other Posts - MemberOtherPosts.csv
   - Party Affiliations - MemberPartyAffiliations.csv
   - Constituency Representations - MemberRepresentations.csv

2. Bills:

   - Latest Stage Regarding A Particular Bill - BillLatestStage.csv
   - All Stages A Particular Bill Has Gone Through - BillAllStages.csv
   - Identifiers For Different Stages - Bill_Stage-Identifier.csv
   - Identifiers For Types of Bill - Bill_Type_Identifiers.csv

3. CommonDivision:

   - Division Happened In The House of Commons - CommonDivision.csv

4. Constituency:

   - Information Regarding Each Constituency - Constituency.csv

5. Publication:

   - HTML Version of Each Publication - Publication_HTML folder

   - PDF Version of Each Publication - Publication_PDF folder

   - Naming Convention for Each Publication File - Publication_Modified.csv

     - For example, consider a file named "1008_3_6814_pdf.pdf". This filename corresponds to specific identifiers within our dataset: "BillId:1008, PublicationType:3, id: 6814". The "id" (6814) serves to distinguish between multiple documents associated with the same BillId and PublicationType. While the "id" itself may not convey any real-life meaning, its combination with the preceding identifiers uniquely identifies a document.

   - Publication Types - Publication_Types.csv

     Generally divided into the following 3 categories:

     - Amendment
     - Committee Debates/Reports
     - Bill Events

   - https://bills.parliament.uk/bills/3554/publications, visit the website to get a feeling of how publications are displayed on a bill website

6. WrittenQA:

   - Written Questions and Answers Published - WrittenQA.csv
   - https://questions-statements.parliament.uk, visit this website for a complete understanding

7. Entire Hansard:

   - Hansard txt files:

     - Common Chamber
     - Westminster Hall
     - Written Statements
     - Petitions
     - Written Corrections

   - It's important to note that the text-based Hansard files are extracted from their original PDF format. This transformation process may occasionally lead to unexpected data formatting issues. To mitigate this, the Hansard Common Chambers text files are directly extracted from the website. This approach aims to resolve any potential data type transformation issues, ensuring data integrity and compatibility.

   - https://hansard.parliament.uk/commons, visit this website to view how Hansard is structured 

     

8. Hansard Common Chambers:

   - Hansard txt files on Common Chambers section exclusively.

### ![ER Diagram.png](https://github.com/JunyiZhou-Conny/Comput-Leg-UK/blob/main/Images/ER%20Diagram.png)

**Q3: What are we missing?**  **Plan for the future**

**A3:** With an abundant amount of data available, missing information requires text analysis techniques to extract useful information out of such them. Specifically, we want the following parts:

1. **Classification of Divisions into 3 categories:**
   
   - **Voice vote getting challenged:** In parliamentary proceedings, a voice vote is when members verbally express their support or opposition to a motion. If this method is challenged, a division is called, requiring members to vote individually. Identifying instances where voice votes are challenged provides insight into contentious issues and the involvement of division requesters.
   - **Unclear result from voice vote:** Occasionally, a voice vote may not produce a clear outcome due to conflicting verbal expressions. Such instances require further clarification through a division to determine the majority opinion.
   - **Identification of key phases:** Certain phrases, such as "Question Put" or "Brought up", often signal an imminent division in parliamentary discussions. Recognizing these key phases helps anticipate upcoming divisions and analyze their context.
   
2. **Oral Questions:**

   Full records of oral questions are available in the Original folder. However, these records may lack consistent organization. Establishing a standardized method to categorize and index oral questions enhances accessibility and facilitates data analysis. This could involve tagging questions by topic, date, member, or any other relevant criteria.

3. **Floor Speeches:**

   Floor speeches are contained within the Hansard Common Chambers. These speeches represent parliamentary debates and discussions on various topics. To effectively extract floor speeches from the Hansard text, natural language processing (NLP) techniques can be employed. NLP algorithms can identify and isolate segments of text that correspond to individual speeches, allowing for further analysis and categorization.

4. **Motion:**

   Motions proposed during parliamentary proceedings may trigger divisions among members. Tracking motions and capturing their occurrence in the Hansard enables the identification of significant parliamentary events and debates. Establishing a systematic approach to detect and document motions ensures comprehensive coverage of parliamentary activities.

### ![Flow Chart.png](https://github.com/JunyiZhou-Conny/Comput-Leg-UK/blob/main/Images/Flow%20Chart%20and%20Missing%20Components.png)



## New Zealand:

**Q1: Where do all of the dataset currently live? How can we access them?**

**A1:** Data are stored in OneDrive.  

As I have disclosed previously, NZ dataset is comparatively much smaller in volume than UK dataset. It shares a similar parlimentary system with UK parliament. The current dataset conforms with the NZ codebook very well, meaning that all the column names fit with the codebook. 

The issue at hand is that I cannot find the source of these data. Despite the consistency and completeness of the dataset we observed, I suspect that this is going to be a potential issue in the future. My preliminary investigaton suggests that NZ parliament has yet to offer API for data retrieval. The best method I could think of is web scraping.

In light of that, I made a similar tutorial regarding how to conduct web scraping on my Github Repo https://github.com/JunyiZhou-Conny/Comput-Leg-UK?tab=readme-ov-file#scraping

**Q2: What do we have?**

**A2:** 

1. Member:

   - Committees Information - nz_committees.csv
   - Committee Membership - nz_committee_membership.csv
   - Constituency information - nz_constituencies.csv
   - Member Information - nz_members.csv
   - Ministries Information - nz_ministries.csv
   - House Membership - nz_constituencies.csv

2. Bills:

   - Bills.csv
   - Bill_events.csv
   - Bill_versions.csv
   - Bill_sop.csv

3. Hansard:

   - Hansard pdf is available from 2000 to 2016

4. Votes:

   - Party Vote - Nz_division.csv
   - Nz_personal_vote.csv

5. WrittenQA:

   - From 47th to 52th parliament

   - Written_Question README

     Each folder contains 5 files:

     XX is a number from 47 to 52 (New Zealand Parliament)

     - XX_a.zip
     - XX_q.zip
     - code_XX.R
     - written_question_XX.Rmd
     - Written_Question_PXX_final.csv


     XX_a: A compressed folder which has all the answers saved individually in each txt file with a unique ID as its name

     XX_q: A compressed folder which has all the questions saved individually in each txt file with a unique ID as its name

     code_XX: R script that scrapped the data from the website to the CSV

     written_question_XX.Rmd: R Markdown that contains data cleaning and feature engineering

     Written_Question_PXX_final.csv: Dataset of the written questions for that particular parliament. Each row consists of issue, date, URL, question_id, answer_id, question_from, question_to.

**Q3: What are we missing? Plan for the future**

**A3:**

1. **Source of Data Investigation**

   This is the most urgent one. If we were able to trace the method of how the previous teams extracted all of the data, then things are going to be much easier. Given the fact that the current data are consistent, following a similar procedure should yield out optimal result that is compatible with the codebook. I believe it is highly beneficial if we can contact students responsible for this previously. the current R code in the folder never reveals the source data. Rather they are merely data maniplation code.


2. **53rd and 54th Parliament Data**

   If we were able to acquire the source of data, then following the same procedure should give us the optimal data. Currently, we only have data from 47th parliament (from 2000) to 52th parliament (ending with 2017). We need new data.



