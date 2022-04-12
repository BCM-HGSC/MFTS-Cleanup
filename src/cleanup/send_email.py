from logging import warning
import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

first_warning = EmailMessage()
first_warning['Subject'] = "Directory Cleanup Warning"
first_warning['From'] = EMAIL_ADDRESS
first_warning['To'] = os.environ.get() # TODO figure out how to obtain this email that's not 'EMAIL_ADDRESS'


first_warning.set_content('
 Hi ____,
 
 
 All files under the folder [link given from directory] as [/share/share/mfts/private/{requestor}/rt{######}] has been shared with the collaborator.
 1 MFTS account has been created. Login information and instructions to download the data has been emailed to the collaborator directly.
 In order to conserve our finite data transfer storage, this data will be kept live for 4 weeks and then purged. Please let us know promptly if the collaborator encounters any problems downloading and validating this data.
 Thank you,
 HGSC
 Baylor College of Medicine
 
')



 with smtplib.smtplib.SMTP_SSL('smtp.rt.hgsc.bcm.edu/', 465) as smtp:
     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
     smtp.send_message(first_warning)


