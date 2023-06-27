#**** Codebase for different method to access GCP ****#

# Imports for all the methods #
import os
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

# 1. Using cmd line gcloud method #
def auth1():
    auth_token = os.popen('gcloud auth print-access-token').read().strip()
    return auth_token

# 2. Using the defualt auth method to get the key using the request #
def auth2():
    creds = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    auth_token = creds.token
    return auth_token

# 3. Using service account key 
def auth3():
    key_path = "<< Service Account Path >>.json"
    credientials = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    return credientials

# 4. Using the defualt direct on GCP Metadata-Flavor service to get the key #
def auth4():
    url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
    header = {"Metadata-Flavor": "Google"}
    r = requests.get(url=url, headers=header)
    r.raise_for_status()
    print("Getting authentication token")
    auth_token = r.json()['access_token']
    return auth_token

# 5. Using the service account and ID token request to sepcific GCP service #
def auth5():
    # URL to specific GCP service #
    url = 'https://{region}-{project-id}.cloudfunctions.net/{cloud-function-name}'

    key_path = "<< Service Account Path >>.json"
    credientials = service_account.IDTokenCredentials.from_service_account_file(key_path, target_audience= url)

    auth_req = google.auth.transport.requests.Request()
    credientials.refresh(auth_req)
    auth_token = credientials.token
    return auth_token

auth_token = auth1()
print(auth_token)