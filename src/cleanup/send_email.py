# from logging import warning
# import os # for interacting with operating system
# import smtplib 
# from email.message import EmailMessage
import argparse

# EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
# EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')
# first_warning = EmailMessage()
# first_warning['Subject'] = "Directory Cleanup Warning"
# first_warning['From'] = EMAIL_SENDER
# first_warning['To'] = os.environ.get('EMAIL_RECEIVER') # TODO figure out how to obtain this email that's not 'EMAIL_ADDRESS'

# #first_warning.set_content(first_email.txt)

# with smtplib.smtplib.SMTP_SSL('smtp.rt.hgsc.bcm.edu/', 465) as smtp:
#      smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
#      smtp.send_message(first_warning)


parser = argparse.ArgumentParser(description='Add Receiving Email')
parser.add_argument("Add sender's email ", type = str)
parser.add_argument("Add receiver email", type= str)
