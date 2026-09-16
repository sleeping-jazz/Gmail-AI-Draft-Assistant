from gmail_auth import get_gmail_service

from gmail_reader_filtered import get_message,parse_message

from ai import classify_email,generate_reply

from gmail_drafts import create_draft

from database import (
    initialize_database,
    is_processed,
    mark_processed
)

def process_email(gmail, message):
    message_id = message["id"]

    if is_processed(message_id):
        print("Already processed. Skipping.")
        return "already_processed"

    email = parse_message(message)
    print()
    print("EMAIL")

    print("From:", email["sender"])
    print("Subject:", email["subject"])

    print()
    print(email["body"])

    print()
    print("Analyzing email...")

    classification = classify_email(email)

    print()
    print("Needs reply:",classification["needs_reply"])

    print("Reason:",classification["reason"])

    if not classification["needs_reply"]:
        print("No reply required.")

        mark_processed(
            message_id=message_id,
            thread_id=email["thread_id"],
            sender=email["sender"],
            subject=email["subject"],
            classification="ignore"
        )
        return "ignored"
    
    print("Generating AI reply...")

    reply = generate_reply(email)

    print()
    print("AI GENERATED REPLY")
    print(reply)
    print()

    answer = input("Create Gmail draft? (y/n): ")

    if answer.lower() != "y":
        print("Draft not created.")
        return "not_created"

    subject = email["subject"]

    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    draft = create_draft(gmail=gmail,
                         to=email["sender"],
                         subject=subject,
                         body=reply,
                         thread_id=email["thread_id"]
                         )

    mark_processed(message_id=message_id,
                   thread_id=email["thread_id"],
                   sender=email["sender"],
                   subject=email["subject"],
                   classification="reply",
                   draft_id=draft["id"]
                   )

    print()
    print("DRAFT CREATED")
    print("Draft ID:", draft["id"])

    return "draft_created"


def service():
    initialize_database()
    gmail = get_gmail_service()

    print("Connected to Gmail.")

    message = get_message(gmail,number_of_messages=1)

    if not message:
        print("No unread emails found.")
        return

    result = process_email(gmail,message)
    print(result)

if __name__ == "__main__":
    service()