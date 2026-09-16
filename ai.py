import json
import ollama


MODEL = "llama3.2:3b"

def classify_email(email):

    prompt = f"""
You are an email triage assistant.

Analyze the following email and determine whether the sender
expects or would reasonably benefit from a response.

Return ONLY a valid JSON. Do not return any other text.

The JSON must have exactly these fields:

{{
    "needs_reply": true or false,
    "reason": "short explanation"
}}

Rules:

- A direct question usually needs a reply.
- A request for information usually needs a reply.
- A meeting request usually needs a reply.
- A conversational/personal email usually needs a reply.
- Newsletters usually do NOT need a reply.
- Advertisements usually do NOT need a reply.
- OTP emails do NOT need a reply.
- Receipts and order confirmations usually do NOT need a reply.
- Automated notifications usually do NOT need a reply.
- Do not assume that every email requires a response.
- When uncertain, prefer needs_reply=false.

FROM: {email["sender"]}

SUBJECT: {email["subject"]}

BODY: {email["body"]}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print(response)
    content = response["message"]["content"].strip()

    try:

        result = json.loads(content)

    except json.JSONDecodeError:

        print("Could not parse classifier response")

        return {
            "needs_reply": False,
            "reason": "Classifier returned invalid JSON."
        }

    return result

def generate_reply(email):

    prompt = f"""
You are an email response assistant.

Write a professional and natural reply to the email below.

IMPORTANT RULES:
- Be concise.
- Do not invent facts.
- Do not make commitments that are not supported by the email.
- Do not claim that the user has completed an action unless the email provides evidence.
- Preserve the general tone of the sender.
- Return ONLY the email body.
- Do not include a subject line.
- Do not include analysis or explanations.

SENDER: {email["sender"]}

SUBJECT: {email["subject"]}

EMAIL: {email["body"]}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    #print(response)
    return response["message"]["content"].strip() #removes unwanted characters from the beginning and end of a string.


if __name__ == "__main__":
    #for testing email classification

    test_emails = [

        {
            "sender": "rahul@example.com",
            "subject": "Meeting tomorrow",
            "body": """
Hi Ayushi,

Can we meet tomorrow at 11 AM to discuss the project?

Regards,
Rahul
"""
        },

        {
            "sender": "newsletter@example.com",
            "subject": "This week's newsletter",
            "body": """
Here are this week's top stories...
"""
        },

        {
            "sender": "amazon@example.com",
            "subject": "order shipped",
            "body": """
Your order #12345 has been shipped.
"""
        }
    ]

    for email in test_emails:

        print("\n" + "=" * 60)

        print("Subject:",email["subject"])

        result = classify_email(email)

        print(result)

    #for testing generate reply

    test_email = {
        "sender": "rahul@example.com",
        "subject": "Meeting tomorrow",
        "body": """
Hi Ayushi,

Can we meet tomorrow at 11 AM to discuss the project?

Regards,
Rahul
"""
    }

    reply = generate_reply(test_email)

    print("\nGenerated reply:")
    print("-" * 60)
    print(reply)
    print("-" * 60)
