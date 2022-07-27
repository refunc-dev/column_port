from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime, date, timedelta
#import sys
import os

os.environ['http_proxy'] = '127.0.0.1:8000'
os.environ['https_proxy'] = '127.0.0.1:8000'

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

def validate_account_info(account_info):
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = f'{os.environ["CP_CONFIG_PATH"]}column-port-service.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)
    # Use the Analytics service object to validate account info.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    exist_account = False
    exist_property = False
    for a in accounts.get('items'):
        if a.get('id') == account_info[0]:
            exist_account = True
            break
    if exist_account == False:
        return 1

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
            accountId=account_info[0]).execute()

    for prop in properties.get('items'):
        if prop.get('id') == account_info[1]:
            exist_property = True
            break
    if exist_property == False:
        return 2

    # Get a list of all views (profiles) for the first property.
    profiles = service.management().profiles().list(
            accountId=account_info[0],
            webPropertyId=account_info[1]).execute()

    for prof in profiles.get('items'):
        if prof.get('id') == account_info[2]:
            exist_profile = True
            return 0
    return 3

def get_results(service, profile_id, path, start, end):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start,
            end_date=end,
            metrics='ga:sessions,ga:goalCompletionsAll',
            dimensions='ga:yearWeek,ga:landingPagePath,ga:yearWeek',
            sort='ga:yearWeek,ga:landingPagePath,ga:yearWeek',
            filters=f'ga:landingPagePath={path}',
            segment='gaid::-5'
            ).execute()

def percentage(part, whole):
    if whole == '0':
        return 0.0
    percentage = 100 * float(part)/float(whole)
    return round(percentage, 1)

def get_analytics_data(path, week, account_info):
    week = week - 1
    day = datetime.now() - timedelta(days=7)
    yr = day.strftime('%Y')
    wk = day.strftime('%U')

    end_day = datetime.strptime(f'{yr}-{wk}-6', '%Y-%U-%u')
    start_day = end_day - timedelta(days=6+(week*7))
    end = end_day.strftime('%Y-%m-%d')
    start = start_day.strftime('%Y-%m-%d')

    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = f'{os.environ["CP_CONFIG_PATH"]}column-port-service.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    #profile_id = get_first_profile_id(service)
    results = get_results(service, account_info[2], path, start, end)
    rows = results.get('rows')
    response = []
    for data in rows:
        date = datetime.strptime(f'{data[2]}-7', '%Y%U-%u')
        response.append({
            'path': data[1],
            'date': date,
            'session':data[3],
            'cv': data[4],
            'cvr': percentage(data[4], data[3])
        })
    return response

def get_analytics_data_eq(path, week, account_info):
    return get_analytics_data(f'={path}', week - 1, account_info)

#if __name__ == '__main__':
#    args = sys.argv
#    if len(args) == 1:
#        path = "/"
#    else:
#        path = args[1]
#
#    print(get_analytics_data_eq(path, 6))