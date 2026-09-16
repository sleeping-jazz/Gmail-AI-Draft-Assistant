import base64
from email.message import EmailMessage

from gmail_auth import get_gmail_service

def create_draft(gmail,to,subject,body,thread_id=None):
    message = EmailMessage()
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    draft_body = {"message": {"raw":encoded_message}}
    
    if thread_id:
        draft_body["message"]["threadId"] = thread_id
        
    draft = gmail.users().drafts().create(
        userId = "me",
        body=draft_body
    ).execute()
    
    return draft

if __name__ == "__main__":
    gmail = get_gmail_service()
    draft = create_draft(
        gmail=gmail,
        to="", # give a valid mail to validate
        subject = "Test AI Draft",
        body = "This is a test draft"
    )
    print("Draft completed successfully")
    print("Draft ID:", draft["id"])