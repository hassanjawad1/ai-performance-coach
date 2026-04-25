import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class CalendarService:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _authenticate(self):
        """Standard Google OAuth2 flow."""
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # You'll need 'credentials.json' from Google Cloud Console
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_todays_context(self):
        """Fetches events for the current day and returns a summary."""
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, timeMax=end_of_day,
            singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return "No meetings today. The schedule is completely clear."

        summary = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_title = event.get('summary', 'Untitled Event')
            summary.append(f"- {event_title} (Starts: {start})")
        
        return "\n".join(summary)

# Singleton instance
calendar_manager = CalendarService()