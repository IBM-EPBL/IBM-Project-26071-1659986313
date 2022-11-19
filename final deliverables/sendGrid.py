import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key='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')
from_email = Email("praj19208.it@rmkec.ac.in")
to_email = To("praj19208.it@rmkec.ac.in")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "okay this no work")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)