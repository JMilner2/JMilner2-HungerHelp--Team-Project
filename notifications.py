"""
Author: Andrew Mason
Description: This code makes it so that when a new post is made, all accounts are notified via email
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models import User


def send_emails():
    # Grab emails from database
    email_list = User.query.filter_by(notifications=True).all()
    # Iterates through list of emails
    for emails in email_list:
        message = Mail(
            from_email='hungerhelphelp@gmail.com',
            to_emails=emails.email,
            subject='Hello From HungerHelp!',
            html_content='<html><body>'
                         '<h1>A new recipe has been posted on our blog!</h1>'
                         '<p>Click the link below to check it out:</p>'
                         '<p><a href="http://127.0.0.1:5000/blog_home">View Blog</a></p>'
                         '<p>Thank you for reading!</p>'
                         '</body></html>')

        # Sendgrid API key connection
        sg = SendGridAPIClient('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')
        response = sg.send(message)

        print(response.status_code)
        print(response.body)
        print(response.headers)
        # Console confirmation
        print(f"Email sent successfully. Response: {response.status_code}")
