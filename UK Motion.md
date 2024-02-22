UK dataset organized in Amazon S3 bucket:https://s3.console.aws.amazon.com/s3/buckets/myukdata?region=us-east-2&bucketType=general&tab=objects

- Private access, require permission from my root account

- <img src="/Users/conny/Library/Application Support/typora-user-images/image-20240118162207522.png" alt="image-20240118162207522" style="zoom:25%;" />

- <img src="/Users/conny/Library/Application Support/typora-user-images/image-20240118162703161.png" alt="image-20240118162703161" style="zoom:25%;" />

- Storing data in Amazon S3 (Simple Storage Service) and Microsoft OneDrive, both popular cloud storage services, offer different advantages and disadvantages based on their features, target audience, and use cases. Here's a comparison:

  ### Advantages of Amazon S3

  1. **Scalability:** Amazon S3 can handle vast amounts of data, making it suitable for businesses and applications that require extensive storage space.
  2. **Durability and Availability:** It offers high durability, ensuring data is not lost, and high availability for accessing data.
  3. **Customizable Security:** Provides advanced security features like bucket policies and Access Control Lists (ACLs).
  4. **Advanced Features:** Offers features like object lifecycle management, versioning, and event notifications.
  5. **Integration with AWS Ecosystem:** Seamless integration with other AWS services for comprehensive cloud solutions.

  ### Disadvantages of Amazon S3

  1. **Cost Complexity:** Pricing can be complex and less predictable due to various factors like storage used, requests made, and data transfer.
  2. **Technical Complexity:** More suitable for users with technical expertise or businesses with IT support.
  3. **Minimal Collaborative Tools:** Lacks direct integration with collaboration tools compared to OneDrive.

  ### Advantages of OneDrive

  1. **Integration with Microsoft Office:** Seamless integration with Office 365 for real-time collaboration and editing.
  2. **User-Friendly Interface:** Easy to use for individuals and businesses without requiring technical expertise.
  3. **Cost-Effective for Small Scale Use:** Suitable for individuals and small businesses due to its straightforward pricing.
  4. **Built-in Collaboration Tools:** Provides features like file sharing and collaborative editing.

  ### Disadvantages of OneDrive

  1. **Limited Advanced Features:** Not as feature-rich as S3 in terms of advanced cloud storage capabilities.
  2. **Storage Limitations:** While sufficient for individuals and small businesses, it might not cater to large-scale storage needs like S3.
  3. **Less Customizable Security:** While it offers good security, it may not be as customizable as Amazon S3.

  ### Conclusion

  - **Amazon S3** is more suited for large-scale, complex applications, especially where integration with other cloud services is important. It's ideal for businesses needing extensive, scalable storage and those who can navigate its technical and pricing complexities.
  - **OneDrive** is better for individual users or small businesses needing straightforward, user-friendly cloud storage, especially if they are already using Microsoft Office products. It offers excellent collaboration tools but is less suitable for large-scale storage needs.

1. Data analysis
   * I think the primary goal for the upcoming semester would be focusing on data analysis. There are a lot of aws services that is probably going to work pretty well. AWS Athena is a service that helps run SQL command directly on strucutured and semi-structured files such as data in formats like CSV, JSON, Parquet, Avro, ORC, and others. In this way, we do not need to worry about constructing the database first. And we can perform python analysis directly 
   * For the current stage, I am using AWS Glue to crawl the existing CSV files for features extraction. A total of 56 tables have been extracted. It is a serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development.
   * For instance, you can query data in S3 using Athena and then use Python for further analysis or visualization.

2. Database Preparation

   * Currently S3 is for data storage, and it is usually for unstrucutured files like images and videos

   * In the future, as our schema is definitively set, we might want to transform our data into a database allowing for SQL performance. Amazon RDS allows for Postgre, MySQL, and a total of 7 management systems

3. Preparation for data hosting

   * Hosting a user interface for data extraction in the future, which probably involves hosting a web in the future. Amazon EC2 instance can have direct access to S3 buckets and all kinds of integrated interactions

   * AWS Lambda enables serverless architectures in the future. For instance, when a user tries to retrieve our data, we can store these information by using Lamda. It is a trigger-based service.



Amazon Textract is a service that automatically extracts text and data from scanned documents. It uses machine learning to read and process a wide range of document types, making it highly effective for converting paper documents or PDFs into machine-readable text. Integrating Amazon Textract with Amazon S3 is a common use case, allowing for the automated processing of documents stored in S3. Here's how it's typically used and how you can combine it with S3:

### How to Use Amazon Textract

1. **Input Document:** The process starts with a document that you want to extract text from. This document could be in formats like PDF, JPEG, or PNG.
2. **Calling Textract:** You can use the Textract API to analyze your document. This involves sending the document to Textract and then receiving the extracted text and data in response.
3. **Data Extraction:** Textract can extract plain text, form data (key-value pairs), and table data. It can also identify and preserve the structure of the document, such as columns, headers, and footers.
4. **Handling Complex Documents:** Textract is particularly useful for processing complex documents like forms or tables, where understanding the layout and relationships between different pieces of text is essential.

### Combining Amazon Textract with Amazon S3

1. **Storing Documents in S3:** Store your documents (like scanned PDFs, images of documents, etc.) in an S3 bucket. This provides a scalable and secure storage solution for your documents.
2. **Triggering Textract from S3:** You can set up an AWS Lambda function to automatically trigger Textract when new documents are uploaded to your S3 bucket. This automation is achieved using S3 event notifications.
3. **Processing with Textract:** The Lambda function calls the Textract API, passing the location (S3 path) of the document to be processed.
4. **Storing Extracted Data:** The extracted text and data can be stored back in S3, or in other AWS services like Amazon RDS or DynamoDB, depending on your use case. You might also want to store the results in a format suitable for further analysis or search, like JSON or CSV.
5. **Further Analysis:** Once the data is extracted and stored, you can use other AWS services (like Amazon Athena, Amazon Redshift, or Amazon Elasticsearch Service) for further analysis, search, and reporting.





UK dataset codes organized in GitHub:https://github.com/JunyiZhou-Conny/Comput-Leg-UK



- Public access to everything except for the API private keys
- ![image-20240118164010908](/Users/conny/Library/Application Support/typora-user-images/image-20240118164010908.png)
- ![image-20240118164022641](/Users/conny/Library/Application Support/typora-user-images/image-20240118164022641.png)