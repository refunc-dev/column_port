from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import sys

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

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

def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None

def get_results(service, profile_id, regex, start, end, term):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start,
            end_date=end,
            metrics='ga:users,ga:sessions,ga:pageviews,ga:goalCompletionsAll',
            dimensions='ga:' + term,
            sort='ga:' + term,
            filters=f'ga:landingPagePath={regex}',
            segment='gaid::-5'
            ).execute()

def percentage(part, whole):
    if whole == '0':
        return 0.0
    percentage = 100 * float(part)/float(whole)
    return round(percentage, 1)

def get_analytics_data(regex, start, end, term):

    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = f'{os.environ["CP_CONFIG_PATH"]}column-port-service.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    results = get_results(service, profile_id, regex, start, end, term)
    rows = results.get('rows')
    print(rows)
    response = []
    for data in rows:
        response.append({
            'regex': regex,
            'term': data[0],
            'users': data[1],
            'session':data[2],
            'pv': data[3],
            'cv': data[4],
            'cvr': percentage(data[4], data[2]),
            'pvr': percentage(data[3], data[2])
        })
    return response

def get_weekly_analytics_data_regex(regex, week):
    week = week - 1
    day = date.today() - timedelta(days=7)
    yr = day.isocalendar().year
    wk = day.isocalendar().week

    end_day = datetime.strptime(f'{yr}-{wk}-6', '%G-%V-%u')
    start_day = end_day - timedelta(days=6+(week*7))
    end = end_day.strftime('%Y-%m-%d')
    start = start_day.strftime('%Y-%m-%d')

    return get_analytics_data(f'~{regex}', start, end, "yearWeek")

def get_monthly_analytics_data_regex(regex, month):
    day = date.today() - relativedelta(months=1)
    past = day.today() - relativedelta(months=month)

    end_day = day.replace(day=calendar.monthrange(day.year, day.month)[1])
    start_day = past.replace(day=1)
    end = end_day.strftime('%Y-%m-%d')
    start = start_day.strftime('%Y-%m-%d')

    return get_analytics_data(f'~{regex}', start, end, "yearMonth")

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        regex = "^/*"
    else:
        regex = args[1]

    print(get_weekly_analytics_data_regex(regex, 6))