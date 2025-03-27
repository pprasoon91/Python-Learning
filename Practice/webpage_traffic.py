#Fetching Traffic Data

from googleapiclient.discovery import build
from google.oauth2 import service_account

# Authenticate
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE = "/home/piyushprasoon/project/Python Learning/Python-Learning/Practice/metal-segment-454405-p7-2686fff1c670.json"

credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
analytics = build('analyticsreporting', 'v4', credentials=credentials)

# Fetch traffic data
response = analytics.reports().batchGet(
    body={
        'reportRequests': [{
            'viewId': 'YOUR_VIEW_ID',
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'metrics': [{'expression': 'ga:sessions'}, {'expression': 'ga:users'}]
        }]
    }
).execute()

print(response)