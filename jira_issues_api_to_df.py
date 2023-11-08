import requests
import pandas as pd
from requests.auth import HTTPBasicAuth


# JIRA CREDENTIALS, STORED
main_jira_domain = SECRETS_DOMAIN_1
main_username = SECRETS_DOMAIN_1_USER
main_api_token = SECRETS_DOMAIN_1_TOKEN
alt_jira_domain = SECRETS_DOMAIN_2
alt_username = SECRETS_DOMAIN_2_USER
alt_api_token = SECRETS_DOMAIN_2_TOKEN


class JiraIssuesService:
  
  # FUNCTION TO GET API URL BASED ON DOMAIN USED
  def JiraIssuesDomainApiUrl (domain):
    jira_issues_url = f'https://{domain}.atlassian.net/rest/api/3/search'
    
    return jira_issues_url

  # FUNCITON FOR ISSUES API GET REQUEST/RESPONSE
  def GetJiraIssues (username, api_token, domain, url):
    auth = HTTPBasicAuth(rd_username, rd_api_token)
    headers = {
      "Accept": "application/json"
    }
    query = {
      # 'jql': f'project = {rd_project_key}',  # Adjust this as needed for specific JQL query
      'fields': 'key, status, issuetype, project, created, updated, priority'
    }
    response = requests.request(
      "GET",
      jira_issues_url,
      headers=headers,
      auth=auth,
      params=query
    )
  
    return response

  # FUNCTION FOR REPONSE TRANSFORMATIONS
  def JiraDataTransformations (data):
    issues = pd.json_normalize(data['issues'])
    select_issues_fields = issues[["key", "fields.status.name", "fields.issuetype.name", "fields.priority.name", "fields.project.name", "fields.created", "fields.updated"]]
    # jira_issues = pd.to_datetime(select_issues[["fields.created", "fields.updated"]], utc=False).dt.tz_localize(None)
  
    return select_issues_fields

  # MAIN FUNCTION TO GET DATA IN DATAFRAME
  def GetIssues (username, api_token, domain):
    api_url = JiraIssuesDomainApiUrl(domain)
    response = GetJiraIssues(username, api_token, domain, api_url)

    if response.status_code == 200:
      data = response.json()
      jira_issues = JiraDataTransformations(data)
    
      return jira_issues

    else:
      break

    print(f'Failed Response, Error Code: {response.status_code}')
