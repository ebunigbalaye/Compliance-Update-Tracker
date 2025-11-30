#This file will be scheduled to run every 7 days and will send compliance updates to subscribers.
from email.message import EmailMessage
import smtplib
import os
from datetime import datetime,timedelta
from app_database import return_articles,return_subscribers

def check_date(pub_date):
    """This checks an article's publication date and only returns 'True'
     if it was published in the past week"""
    pub_date= datetime.strptime(pub_date,"%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
    start_date = datetime.now()-timedelta(weeks=1)
    end_date = datetime.now()
    if start_date<= pub_date<=end_date:
        return True
    return False



def send_email(name,email,gmail_server):
    message = EmailMessage()
    message['From'] = "ebunoluwaigbalaye.com"
    message['To'] = email
    message['Subject'] = "Compliance News Tracker"
    content = f"""Hey {name},
Here are your updates for this week,
"""
    articles = return_articles()
    for article in articles:
          if check_date(article.pub_date) and article.compliance:
                content += f"""
Title: {article.title}
Published on : {article.pub_date[4:17]}
{article.link}
Article Overview:
{article.description[:-5].strip()+"...."}
"""
                content+= '\n'
   
    message.set_content(content)
    gmail_server.send_message(message,email)


if __name__ == 'main':
     with smtplib.SMTP_SSL('smtp.gmail.com',port=465) as my_gmail_server:
                    # Getting email password
                    subscribers=return_subscribers()
                    password = os.getenv('gmail_access_key')
                    my_gmail_server.login('ebunigbalaye@gmail.com',password)
                    for subscriber in subscribers:
                          send_email(subscriber.name,subscriber.email,my_gmail_server)


