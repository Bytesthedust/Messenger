# Messenger
A small script that sends a cybersecurity focused newsletter to your email

# Purpose
This script was made to address a problem of wanting to read multiple cybersecurity articles but not having the time to scan every reputable news source. 

# Process
The script is set to be executed every Sunday through Task Scheduler and will access a news source api and collect every article related to cybersecurity from a number of sources from the past week.

# Dependencies
NewsApiClient from newsapi - news source api


newsapi.newsapi_exception from NewsAPIException - exception handling


datetime, timedelta from datetime - calculating dates for article search


smtplib - send email


MIMEMultipart from email.mime.multipart - construction of email parameters and content


MIMEText from email.mime.text - construction of email parameters and content


os - access env key-pairs


dotenv - load env key-pairs

# Installation
1. Clone the repository
2. Install the required dependencies: pip install newsapi-python python-dotenv

# Usage
1. Set up api key and email credentials in a .env file
2. Use Task Scheduler or similar app to set up execution triggers and conditions

# Error Handling
In the case of an error in reading in the articles, an error email will be sent instead to provide information on resolving the error

# Notes
An api key from NewsApi is required to use this script. A key can be registered at their website: https://newsapi.org/
This program also uses an unofficial python client library which can be found on the creator's repository: https://github.com/mattlisiv/newsapi-python
