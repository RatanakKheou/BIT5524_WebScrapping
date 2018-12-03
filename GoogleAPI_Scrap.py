from __future__ import print_function
from datetime import timedelta
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import numpy as np


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    page_token = None
    calendar_ids = []

    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendar_ids.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


   # This code is to look for all-day events in each calendar for the month of September
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
    # You need to get this from command line
    # # Bother about it later!
    #     now = datetime.datetime.utcnow() + timedelta(days = 7)
    #     now = now.isoformat() + 'Z' # 'Z' indicates UTC time
    start_date = datetime.datetime(
        2016, 01, 01, 00, 00, 00, 0).isoformat() + 'Z'
    end_date = datetime.datetime(2018, 12, 01, 23, 59, 59, 0).isoformat() + 'Z'
    eventID = []
    Dates = []
    Days = []
    CategoryID = []
    for calendar_id in calendar_ids:
        count = 0
        print('\n----%s:\n' % calendar_id)
        eventsResult = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
    for event in events:
        eventDate = event['start'].get('dateTime', event['start'].get('date'))
        eventTitle = event['summary']
        print(type(eventDate), eventTitle)
        weekDays = datetime.datetime.strptime(eventDate,"%Y-%m-%d").weekday()
        Dates.append(eventDate)
        eventID.append(eventTitle)
        Days.append(numToDays(weekDays))
        CategoryID.append('Special')
    toFile = pd.DataFrame(np.column_stack([eventID, CategoryID, Dates, Days]), columns = ['Events', 'CategoryID', 'Date', 'Days'])
    fileName = '{}{}.csv'.format("C:\\Users\\krata\\Documents\\BIT 5524\\Scrapping\\", "events_2018-12-3")
    toFile.to_csv(fileName, index = False)

def numToDays(shortMonth):
    return{
            0 : 'Sunday',
            1 : 'Monday',
            2 : 'Tuesday',
            3 : 'Wednesday',
            4 : 'Thursday',
            5 : 'Friday',
            6 : 'Saturday',
    }[shortMonth]

if __name__ == '__main__':
    main()
