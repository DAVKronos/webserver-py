# TO RUN: sudo docker compose run --rm python python3 -m app.test.test-google-api
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'google-api.json'
ADMIN_EMAIL = 'webmaster@kronos.nl'

# Required scope for reading Google Groups / mailing lists
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.readonly']


def list_mailing_lists():
    try:
        # Load credentials from the private key and set the subject (admin user to impersonate)
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        ).with_subject(ADMIN_EMAIL)

        # Build the Admin SDK Directory service client
        service = build('admin', 'directory_v1', credentials=creds)

        print("Fetching mailing lists (Google Groups)...")
        
        # 'my_customer' is a special alias for your Google Workspace account domain
        results = service.groups().list(customer='my_customer').execute()
        groups = results.get('groups', [])

        if not groups:
            print('No mailing lists found.')
            return

        print(f"\nFound {len(groups)} mailing list(s):")
        print("-" * 50)
        for group in groups:
            # name = group.get('name', 'N/A')
            # email = group.get('email', 'N/A')
            # description = group.get('description', 'No description')
            # print(f"Name:        {name}")
            # print(f"Email:       {email}")
            # print(f"Description: {description}")
            # print("-" * 50)
            print(group)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    list_mailing_lists()