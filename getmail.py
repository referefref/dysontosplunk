#!/usr/bin/python3
import email, getpass, imaplib, os

detach_dir = '.' # directory where to save attachments (default: current)
user = ""
pwd = ""

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
#print(m.list())
m.select('"Vacuum"') # where you autoput your vacuum photos

resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id

for i in items:
	print(i, end = ' ')

count = 1
for emailid in items:
#for finalid in range(1, 420):
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content

    download_folder="/home/user/vacuum" #put your install location here

    msg = email.message_from_bytes(data[0][1])
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        att_path = os.path.join(download_folder, str(count) + ".jpg")

        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

    m.store(emailid,'+FLAGS', '(\\Deleted)')

    count=count + 1

m.expunge()
m.close()
m.logout()
