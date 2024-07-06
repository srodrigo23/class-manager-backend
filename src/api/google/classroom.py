

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def google_authorization() -> None:
  SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly", 
    "https://www.googleapis.com/auth/classroom.courses", 
    "https://www.googleapis.com/auth/classroom.profile.emails",
    "https://www.googleapis.com/auth/classroom.rosters", 
    "https://www.googleapis.com/auth/classroom.profile.emails"
  ]

  creds = None
  
  token_path       = './token.json'
  credentials_path = './credentials.json'

  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open(token_path, "w") as token: 
      token.write(creds.to_json())
  return creds

courseId = '616805243112'

def get_courses()->list:
  creds = google_authorization()
  try:
    service = build("classroom", "v1", credentials=creds)
    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])

    if not courses:
      return []
    return courses
    # Prints the names of the first 10 courses.
    # print("Courses:")
    # for course in courses:
    #   print(course["name"])
  except HttpError as error:
    print(f"An error occurred: {error}")


def get_students_list(class_code:str)-> list:
  creds = google_authorization()
  try:
    service = build("classroom", "v1", credentials=creds)
    results = service.courses().students().list(
      courseId=courseId,
      pageToken=None, 
      x__xgafv=None
    ).execute()
    i = 0
    students = results.get("students", [])
    students_list = []
    if not students:
      return []
    for student in students:
      i=i+1
      students_list.append((i, student["profile"]['name']['fullName'], student["profile"]['emailAddress']))
    while True:
      nextToken = results.get("nextPageToken", [])
      if nextToken:
        results = service.courses().students().list(
          courseId=courseId, 
          pageSize=300, 
          pageToken=nextToken, 
          x__xgafv=None).execute()
        students = results.get("students", [])
        if not students:
          return students_list
        for student in students:
          i = i + 1
          students_list.append((i, student["profile"]['name']['fullName'], student["profile"]['emailAddress']))
      else:
        break
    return students_list
  except HttpError as error:
    print(f"An error occurred: {error}")
  