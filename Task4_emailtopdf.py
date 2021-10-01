import email
import imaplib
import os
import mimetypes
import pdfkit
username='vidyakailasamp@gmail.com'
password='Vidyakpa'
mail=imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username,password)
mail.select("inbox")
result,data=mail.uid('search',None,"ALL")
inbox_items=data[0].split()
most_recent=inbox_items[-1]
oldest=inbox_items[0]
result2, email_data=mail.uid('fetch',most_recent,'(RFC822)')
raw_email=email_data[0][1].decode("utf-8")
email_msg=email.message_from_string(raw_email)
to_=email_msg['To']
from_=email_msg['from']
subject_=email_msg['subject']
date_=email_msg['date']
counter=1#if email_msg.get_content_maintype() == 'multipart':
for part in email_msg.walk():
        print ("inside for loop")
        if part.get_content_maintype() == 'multipart':
            print ("inside 1st if")
            continue
        """if part.get('Content-Disposition') is None:
            print ("inside 2nd if")
            continue """
        print(part.get_content_type())
        filename=part.get_filename()
        print(filename)
        if filename is not None:
            sv_path = os.path.join(os.getcwd(), filename)
            if not os.path.isfile(sv_path):
                print (sv_path )
                fp = open(sv_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        else:
              content_type=part.get_content_type()
              if 'html' in content_type:
                   ext='.html'
              elif 'plain' in content_type:
                   ext='.txt'
              filename='msg-part-%08d%s' %(counter,ext)
              save_path=os.path.join(os.getcwd(),"emails",date_,content_type)
              if not os.path.exists(save_path):
                   os.makedirs(save_path)
              with open(os.path.join(save_path,filename),'wb') as fp:
                  fp.write(part.get_payload(decode=True))
              pdfkit.from_file(os.path.join(save_path,filename),from_+""+date_+'.pdf')
        counter+=1
