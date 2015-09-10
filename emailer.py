import smtplib
from email.mime.text import MIMEText


def prompt(prompt_text):
	return input(prompt_text).strip()

me = prompt("Gmail Username: ")
pw = prompt("Gmail Password: ")

recipients = "arohrer6@gmail.com"


with open("generated-data/NFLpicks.html") as picks:
	html = """\
<html>
	<head></head>
	<body>
		<p>	Hey, these are the picks for this week formatted into a table.
			If you'd like any formatting changes, let me know.
		</p>
		<div class="container">
			{}
		</div>
	</body>
</html>
"""
	msg = MIMEText(html.format(picks.read()), 'html')

msg['Subject'] = 'NFL Picks'
msg['From'] = "the god"
msg['To'] = recipients

s = smtplib.SMTP('gmail.com')
s.ehlo()
s.starttls()
s.login(me, pw)
s.sendmail(msg)
s.quit()
