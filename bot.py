import settings
import socket
import _thread
import re
from time import sleep
from email_sender import Email_Sender

class Bot():
	def __init__(self, host, port, channel, username, password):
		self.host = host
		self.port = port
		self.channel = channel
		self.username = username
		self.password = password
		self.socket = socket.socket()
		self.SEND_PATTERN= r"^!send [\w_\-\.]+@[\w_\-\.]+\.[a-z]{2,6}$"
		self.email_sender = Email_Sender()

	def connect(self):
		self.socket.connect((self.host, self.port))
		self.socket.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
		self.socket.send("PASS {}\r\n".format(self.password).encode("utf-8"))
		self.socket.send("NICK {}\r\n".format(self.username).encode("utf-8"))
		self.socket.send("JOIN #{}\r\n".format(self.channel).encode("utf-8"))

	def run(self):
		while True:
			try:
				response = self.socket.recv(1024).decode("utf-8")
			except Exception as E:
				pass
			if response == "PING :tmi.twitch.tv\r\n":
				self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			else:
				message = []
				if re.search(r"PRIVMSG #[\w_]+ :\w*", response):
					edited_response = re.split(r"PRIVMSG #\w+ :", response)
					message = edited_response[1].strip()
					sub = self.user_is_subscriber(response)
					self.reply(message, sub)
		sleep(1)

	def reply(self, message, sub):
		if re.match(self.SEND_PATTERN, message) != None and sub != None:
			strings = message.split(" ")
			self.send_email(strings[1])
			self.send_message("Письмо доставлено на {}".format(strings[1]))

	def user_is_subscriber(self, response):
		is_subscriber = re.search(r"subscriber=1", response)
		return is_subscriber
		
	def send_message(self, message):
		self.socket.send("PRIVMSG #{} :{}\r\n".format(self.channel, message).encode("utf-8"))

	def send_email(self, email):
		self.email_sender.send(email)
		
