import requests
import json

flex_login = 'business-intelligence@rentdynamics.com'
flex_pass = 'QYC!anv_gpx0meu3mqu'
twilio_workspace_id = 'fqh3dx3v2sz4n7imop00szjn1d3gt0au'
twilio_object_id = '3841209'


def prep_downloaded_format_to_csv(data):
    lines = data.strip().split('\n')
    header = lines[0].split(',')
    data = [line.split(',') for line in lines[1:]]
    formatted_data = [dict(zip(header, row)) for row in data]

    return formatted_data


def get_flex_api_auth(login_cred, pass_cred):
    headers = \
        {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    json_data = \
        {
            'postUserLogin':
                {
                    'login': login_cred,
                    'password': pass_cred,
                    'remember': 0,
                    'verify_level': 2,
                },
        }

    response = requests.post('https://analytics.ytica.com/gdc/account/login', headers=headers, json=json_data)
    data = json.loads(response.text)

    super_secure_token = data['userLogin']["token"]
    return super_secure_token


def get_flex_temp_token(ss_token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-GDC-AuthSST': ss_token,
    }

    response = requests.get('https://analytics.ytica.com/gdc/account/token', headers=headers)
    data = json.loads(response.text)

    temp_token = data['userToken']['token']
    return temp_token


def get_flex_uri(workspace_id, object_id, temp_token):
    cookies = {
        'GDCAuthTT': temp_token,
    }
    headers = {
        'Accept': 'application/json',
    }
    json_data = {
        'report_req': {
            'report': '/gdc/md/' + workspace_id + '/obj/' + object_id,
        },
    }

    response = requests.post('https://analytics.ytica.com/gdc/app/projects/' + workspace_id + '/execute/raw', cookies=cookies,
                             headers=headers, json=json_data)

    data = json.loads(response.text)
    uri_link = data['uri']

    return uri_link


def download_flex_insights_report(uri_id, temp_token):
    cookies = {
        'GDCAuthTT': temp_token,
    }
    headers = {
    }

    response = requests.get('https://analytics.ytica.com/' + uri_id, cookies=cookies, headers=headers)
    data = response.json()

    result = prep_downloaded_format_to_csv(data)
    # json_result = json.dumps(result, indent=4)
    # csv = json.loads(result)
    # return csv
    return result


def flex_insights_csv(login, password, workspace_id, obj_id):
    sst = get_flex_api_auth(login, password)
    tt = get_flex_temp_token(sst)
    uri = get_flex_uri(workspace_id, obj_id, tt)
    csv = download_flex_insights_report(uri, tt)

    return csv


final_output = flex_insights_csv(flex_login, flex_pass, twilio_workspace_id, twilio_object_id)
print(final_output)
