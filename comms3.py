#!/usr/bin/python
import os
import datetime
import boto
from boto.s3.key import Key
import tinys3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class comms3:

	def upload(self, bucket, filename):
		print 'Trying to connect ...........'
		conn = tinys3.Connection('access_key','Secret_key',tls=True)
		print "Connected to Ranganath's account .................."

		print 'Uploading the file' + filename + ' to' + bucket + ' bucket' + '.................'
		f = open(filename,'rb')
		conn.upload(filename,f,bucket)
		print 'Done!'

	def download(self, bucket, filename):
		print "Trying to connect ............."
		conn = boto.connect_s3('access_key','secrete_key')

		print "Successfully connected to Ranganath's Account ...................."
		print "Listing the buckets available ............."

		bucket = conn.get_bucket(bucket, validate = False)
		key = Key(bucket, filename)
		headers = {}
		if os.path.isfile(filename):
			print "File exists, adding If-Modified-Since header"
			modified_since = os.path.getmtime(filename)
			timestamp = datetime.datetime.utcfromtimestamp(modified_since)
			headers['If-Modified-Since'] = timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
		try:
			print 'Downloading the file .................'
			key.get_contents_to_filename(filename, headers)
		except boto.exception.S3ResponseError as e:
			print 'entered except block .........'
			print e
			return 304
		return 200
	
	def email(self):
		# me == my email address
		# you == recipient's email address
		me = "Ranganath.Kulkarni@harman.com"
		you = "Ranganath.Kulkarni@harman.com"

		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "S3TestMail"
		msg['From'] = me
		msg['To'] = you

		# Create the body of the message (a plain-text and an HTML version).
		text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
		html = """\
		<html>
			<head></head>
			<body>
			<p>Hi!<br>
				How are you?<br>
				Here is the <a href="http://www.python.org">link</a> you wanted.
			</p>
			</body>
		</html>
		"""

		# Record the MIME types of both parts - text/plain and text/html.
		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		msg.attach(part1)
		msg.attach(part2)

		# Send the message via local SMTP server.
		s = smtplib.SMTP('webmail.harman.com/owa')
		# sendmail function takes 3 arguments: sender's address, recipient's address
		# and message to send - here it is sent as one string.
		s.sendmail(me, you, msg.as_string())
		s.quit()


obj = comms3()
obj.download('ranganathk4', 's3samplefile.txt')
obj.upload('ranganathk4', 's3uploadfile.txt')
#obj.email()
