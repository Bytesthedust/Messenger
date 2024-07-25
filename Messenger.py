# Name: Kevon Nelson
# Date: 7-21-24
# Version: 1.0.0
# Purpose: Search news sources for cybersecurity related articles and send them as an email

# IMPORT LIBRARIES
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# LOAD ENV VALUES
load_dotenv()

# SETTING DATA PARAMETERS
current_date = datetime.now()
prev_week = current_date - timedelta(days=6)

current_date_format = current_date.strftime('%Y-%m-%d')
prev_week_format = prev_week.strftime('%Y-%m-%d')

# SET EMAIL PARAMETERS
user_email = os.getenv("EMAIL_USR")
user_psw = os.getenv("EMAIL_PSW")
smtp_server = 'smtp.mail.yahoo.com' # Change to preferred email provider
smtp_port = 587 # default and secure port for SMTP

# CREATE EMAIL CONTENT
def create_email_content(sender, recipient, subject, html_content):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    return msg

# FORMAT EMAIL
def format_articles_html(articles):
    html_content = f"<h1>{prev_week_format}-{current_date_format} Cybersecurity News</h1>"
    for article in articles:
        html_content += f"""
        <h2>{article['title']}</h2>
        <p><strong>Description:</strong> {article['description']}</p>
        <p><strong>Source:</strong> {article['source']['name']}</p>
        <p><strong>URL:</strong> <a href="{article['url']}"> {article['url']}</a></p>
        <hr>
        """
    return html_content

# FORMAT ERROR EMAIL
def format_error_email(errorStatus, errorCode, errorMsg):
    html_content = f"<h2>Messenger Error Notification</h2>"
    html_content += f"""
    <p> An error has occured while fetching articles. Please resolve as soon as possible</p>
    <p><strong>Status:</strong> {errorStatus}</p>
    <p><strong>Code:</strong> {errorCode}</p>
    <p><strong>Message:</strong> {errorMsg}</p>
    """
    return html_content

# SEND EMAIL
def send_email(msg):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() #encryption of SMTP
        server.login(user_email, user_psw)
        server.sendmail(user_email, user_email, msg.as_string())
        server.quit()
        print("Email sent sucessfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ACCESS NEWS API
key = os.getenv("API_KEY")
newsapi = NewsApiClient(api_key = key)

# FETCH ARTICLES
try:
    all_articles = newsapi.get_everything(q = 'cybersecurity OR glitch OR outage OR hack OR hacked OR hacker OR breach OR bug',
                                      sources = 'ars-technica,bbc-news,wired,the-verge',
                                      from_param = prev_week,
                                      to= current_date,
                                      language= 'en',
                                      sort_by='relevancy')
    if all_articles:
        articles = all_articles['articles']
        html_content = format_articles_html(articles)
        msg = create_email_content(user_email, user_email, "Sunday Cybersecurity News", html_content)
        send_email(msg)

except NewsAPIException as e: 

    # If an exception occurs, an error email will be sent to notify the user
    html_content = format_error_email(e.exception["status"], e.exception["code"], e.exception["message"])
    msg = create_email_content(user_email, user_email, "Messenger Error Notification", html_content)
    send_email(msg)
except Exception as e:
    print(f"An unexpected error has occured: {e}")
