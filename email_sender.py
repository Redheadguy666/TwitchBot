import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email_Sender():
	def __init__(self):
		self.smtp_server = settings.SMTP_SERVER
		self.port = settings.SMTP_PORT
		self.login = settings.SMTP_LOGIN
		self.password = settings.SMTP_PASSWORD
		
	def send(self, email, message = settings.SMTP_MESSAGE):
		FROM = self.login
		TO = email
		msg = MIMEMultipart()
		msg["From"] = FROM
		msg["To"] = TO
		msg["Subject"] = "Телеграм Оляши"
		body = message
		msg.attach(MIMEText(body, "plain"))

		server = smtplib.SMTP(self.smtp_server, self.port)
		server.starttls()
		server.login(self.login, self.password)
		server.sendmail(FROM, TO, str(msg))



