import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .models import Facility, BoothEvent

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SCHEDULE_SPREADSHEET_ID = '1CWqQLyVADwE-IwaGHHW9iChGhSsdyoSJrNfZMxER11I'
THEATER_SHEET_NAME = 'Theater'


def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def get_theater_slots(service) -> Facility:
    FACILITY_NAME = 'Theater'

    # Row indices
    DATE = 0
    TIME_FROM = 1
    TIME_TO = 2
    WHO = 3
    WHAT = 4
    CONFIRMED = 5

    # Dates
    THURSDAY = '5/2'
    FRIDAY = '5/3'
    SATURDAY = '5/4'

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SCHEDULE_SPREADSHEET_ID,
                                range=THEATER_SHEET_NAME).execute()
    values = result.get('values', [])

    facility = Facility(title=FACILITY_NAME)

    if not values:
        return facility

    for row in values:
        if row[CONFIRMED] != '1':
            continue

        event = BoothEvent(
            start=row[TIME_FROM],
            finish=row[TIME_TO],
            title=row[WHAT],
            who=row[WHO]
        )

        date = row[DATE]

        if date == THURSDAY:
            facility.thursday.append(event)
        elif date == FRIDAY:
            facility.friday.append(event)
        elif date == SATURDAY:
            facility.saturday.append(event)

    return facility
