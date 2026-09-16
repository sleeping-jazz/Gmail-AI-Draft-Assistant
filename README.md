# Gmail AI Draft Assistant

An AI-powered Gmail assistant that reads unread emails, determines whether they require a reply, generates a suitable response, and saves the response as a Gmail draft.

The application uses the Gmail API for accessing emails, Ollama for AI-powered classification and reply generation, and SQLite to keep track of emails that have already been processed.

## Features

* Connects to Gmail using Google OAuth 2.0
* Reads unread emails
* Checks whether an email has already been processed
* Uses AI to determine whether a reply is required
* Generates a suggested reply using Ollama
* Lets the user review the generated reply before creating a draft
* Saves the generated response as a Gmail draft
* Uses SQLite to prevent the same email from being processed again

## How It Works

```text
Unread Gmail Email
        |
        v
    Gmail API
        |
        v
Check SQLite Database
        |
   Already processed?
      /       \
    Yes        No
    |           |
   Skip         v
           Parse Email
                |
                v
        AI Classification
                |
        Needs a reply?
          /          \
        No            Yes
        |              |
        v              v
   Mark in SQLite   Generate Reply
                       |
                       v
                User Confirmation
                       |
                  Create Draft
                       |
                       v
                 Save in SQLite
```

## Technologies Used

* Python 3.12+
* Gmail API
* Google OAuth 2.0
* Ollama
* Llama 3.2 3B
* SQLite

## Requirements

Before running the project, make sure the following are installed or available:

* Python 3.12 or newer
* A Google account
* A Google Cloud project
* Gmail API enabled
* Google OAuth 2.0 credentials
* Ollama
* Llama 3.2 3B model

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/sleeping-jazz/Gmail-AI-Draft-Assistant>
cd <Gmail-AI-Assistant>
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Google Gmail API Setup

This project uses the Gmail API to read emails and create drafts.

### 1. Create a Google Cloud Project

Create a project in Google Cloud Console.

### 2. Enable the Gmail API

Enable the Gmail API for the project.

### 3. Configure the OAuth Consent Screen

Configure the OAuth consent screen for the application.

The application currently requests the following Gmail scope:

```text
https://www.googleapis.com/auth/gmail.modify
```

### 4. Create OAuth Credentials

Create an OAuth 2.0 Client ID for a Desktop application.

Download the credentials file and place it in the root directory of the project.

Rename the file to:

```text
credentials.json
```

**Do not upload `credentials.json` to GitHub.**

The application uses this file during the initial Google authentication process.

After authentication, Google OAuth generates a local `token.json` file for subsequent authentication.

## Google OAuth Testing

If the Google Cloud OAuth application is in **Testing** mode, the Gmail account being used must be added as a test user in the Google Cloud OAuth configuration.

Therefore, users who want to test the application may need to provide their Google account email address to the project owner so that the account can be added as a test user.

For wider public distribution, the Google OAuth configuration should be reviewed according to Google's requirements for the Gmail scopes being used.

## Ollama Setup

The project uses Ollama to run the AI model locally.

Install Ollama and make sure it is running.

Then download the model used by the application:

```bash
ollama pull llama3.2:3b
```

The application currently uses the `llama3.2:3b` model for both email classification and reply generation.

## Running the Application

After completing the setup, activate the virtual environment and run:

```bash
python draft_assistant_final.py
```

On the first run, the application will start the Google OAuth authentication process.

After successful authentication, the application can access the authorized Gmail account.

## Processing Workflow

The current version processes **one unread email per execution**.

For each email, the application:

1. Retrieves an unread email from Gmail.
2. Checks its message ID against the SQLite database.
3. Skips the email if it has already been processed.
4. Parses the email information.
5. Sends the email to the AI classifier.
6. Determines whether the email requires a reply.
7. Stores emails that do not require a reply as processed.
8. Generates an AI reply if a response is required.
9. Displays the generated reply.
10. Asks the user whether a Gmail draft should be created.
11. Creates the draft if the user confirms.
12. Stores the processed email and draft information in SQLite.

The application does **not** automatically send emails. Generated responses are saved as drafts so that the user can review them before sending.

## SQLite Database

SQLite is used to keep track of processed emails.

The application automatically creates a local database:

```text
assistant.db
```

The database contains a `processed_emails` table that stores information such as:

* Message ID
* Thread ID
* Sender
* Subject
* Classification
* Draft ID
* Processing timestamp

The message ID is used to determine whether an email has already been processed.

The database is local to each installation and should not be uploaded to GitHub.

## Project Structure

```text
gmail-ai-draft-assistant/
├── README.md
├── requirements.txt
├── .gitignore
├── draft_assistant_final.py
├── gmail_auth.py
├── gmail_reader_filtered.py
├── gmail_drafts.py
├── ai.py
└── database.py
```

### File Descriptions

| File                       | Purpose                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `draft_assistant_final.py` | Main application and processing workflow                     |
| `gmail_auth.py`            | Handles Gmail OAuth authentication and Gmail API connection  |
| `gmail_reader_filtered.py` | Retrieves and parses unread Gmail messages                   |
| `gmail_drafts.py`          | Creates Gmail drafts                                         |
| `ai.py`                    | Classifies emails and generates replies using Ollama         |
| `database.py`              | Creates and manages the SQLite database                      |
| `requirements.txt`         | Lists required Python packages                               |
| `.gitignore`               | Prevents sensitive and unnecessary files from being uploaded |

## Security

Do not commit the following files to GitHub:

```text
credentials.json
token.json
assistant.db
```

These files may contain authentication credentials, authorization tokens, or data related to processed emails.

The `.gitignore` file is configured to prevent these files from being accidentally committed.

## Privacy

The application accesses Gmail messages to determine whether they require a response and to generate draft replies.

Users should review the Gmail permissions requested during the OAuth authorization process.

If using Ollama locally as configured, the AI model runs on the user's machine.

AI-generated replies should be reviewed before being sent.

## Limitations

The current version:

* Processes one unread email per execution.
* Requires Google OAuth authorization.
* Requires the Gmail account to be an authorized test user if the OAuth application is in testing mode.
* Requires Ollama and the `llama3.2:3b` model.
* Generates drafts but does not automatically send emails.
* Primarily extracts plain-text email content.

## Future Improvements

Possible improvements include:

* Processing multiple unread emails in a single execution
* Adding a graphical or web-based interface
* Allowing users to select different AI models
* Improving HTML email parsing
* Supporting email attachments
* Adding customizable reply styles
* Improving email classification
* Adding better handling for long email threads

## Disclaimer

This project is intended for educational and experimental purposes.

AI-generated responses may contain mistakes or inappropriate suggestions. Always review a generated draft before sending it.
