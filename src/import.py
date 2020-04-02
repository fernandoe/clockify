import csv
import json
import os
import sys
from datetime import datetime, timedelta

import requests

API = "https://api.clockify.me/api/v1"
API_WORKSPACES = f"{API}/workspaces"
API_PROJECTS = f"{API}/workspaces/%s/projects"
API_TIME_ENTRIES = f"{API}/workspaces/%s/time-entries"

PROJECT_ID = os.environ.get("PROJECT_ID")
WORKSPACE_ID = os.environ.get("WORKSPACE_ID")

HEADERS = {
    "X-Api-Key": os.environ.get("API_KEY"),
    "Content-Type": "application/json"
}


def user():
    response = requests.get(f"{API}/user", headers=HEADERS)
    print(json.dumps(response.json()))


def workspaces():
    response = requests.get(API_WORKSPACES, headers=HEADERS)
    print(json.dumps(response.json()))


def projects(workspace: str):
    response = requests.get(API_PROJECTS % workspace, headers=HEADERS)
    print(json.dumps(response.json()))


def import_records(filepath: str, project_id: str):
    with open(filepath) as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # skip the header
        for row in reader:
            print(row)
            description = row[5]
            start = format_datetime_entry(f"{row[7]}T{row[8]}")
            end = format_datetime_entry(f"{row[9]}T{row[10]}")
            data = {
                "billable": "true",
                "description": description,
                "projectId": project_id,
                "start": start,
                "end": end
            }
            print(json.dumps(data, indent=4))
            response = requests.post(API_TIME_ENTRIES % WORKSPACE_ID, json=data, headers=HEADERS)
            print_response(response)


def print_response(response):
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json())}")
    else:
        print(f"Response: {response.content}")


def import_into_clockify(filepath):
    # user()
    # workspaces()
    # projects(PROJECT_ID)
    import_records(filepath, PROJECT_ID)


def format_datetime_entry(datetime_entry):
    date = datetime.fromisoformat(datetime_entry)
    date = date + timedelta(hours=3)
    return f"{date.isoformat()}Z"


if __name__ == '__main__':
    import_into_clockify(sys.argv[1])
