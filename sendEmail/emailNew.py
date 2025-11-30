from email.message import EmailMessage
from sendEmail.emailExisting import *
from app_database import return_articles
#This is the email that will  be sent to new users to welcome them.

def send_email(name,email,gmail_server):
    message = EmailMessage()
    message['From'] = "ebunoluwaigbalaye.com"
    message['To'] = email
    message['Subject'] = "Compliance News Tracker"
    body = f"""
Hey {name},

Thanks for signing up!

Just wanted to say hi and let you know that you’re all set. From now on, you’ll get weekly updates with the latest compliance news.

In the meantime, here are some updates from the past week:
{test_articles()}

Catch you soon!
"""

    message.set_content(body)
    gmail_server.send_message(message,email)


def test_articles():
    """This function returns compliance related articles from the past week
    and formats the contents into a form that will then be sent by email to new subscribers."""
    articles = return_articles()
    content = ""
    for article in articles:
         if check_date(article.pub_date) and article.compliance:
            content += f"""
Title: {article.title}
Published on : {article.pub_date[4:17]}\n
Article Description:
{article.description[18:-5].strip()+"...."}\n
{article.link}\n
"""
    return content