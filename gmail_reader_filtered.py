import base64
from gmail_auth import get_gmail_service

def get_message(gmail,number_of_messages,query="is:unread"):
    response = gmail.users().messages().list(
        userId="me",
        maxResults=number_of_messages,
        q=query
    ).execute()
    
    messages= response.get("messages",[])
    
    if not messages:
        return None
    message_id= messages[0]["id"]
    message=gmail.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()
    return message

def get_headers(message):
    headers = message['payload'].get('headers',[])
    result={}
    for header in headers:
        name=header["name"].lower()
        if name in {"from","to","cc","subject","date"}:
            result[name]= header["value"]
    return result

def extract_text_from_payload(payload):
    body = ""
    
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
    else:
        data = payload["body"].get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8")
    
    return body

def parse_message(message):
    headers = get_headers(message)
    body = extract_text_from_payload(message["payload"])
    
    email = {
        "id": message["id"],
        "thread_id": message["threadId"],
        "sender": headers.get("from",""),
        "to": headers.get("to",""),
        "cc": headers.get("cc",""),
        "subject": headers.get("subject",""),
        "date": headers.get("date",""),
        "body": body
    }
    return email



if __name__ == "__main__":
    gmail = get_gmail_service()

    message= get_message(gmail,number_of_messages=2)
    
    email = parse_message(message)
    
    print("From:", email["sender"])
    print("Subject:", email["subject"])
    print("Date:", email["date"])
    print(email["body"][:1000])