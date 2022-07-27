from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import os

os.environ['http_proxy'] = 'http://127.0.0.1:8000'
os.environ['https_proxy'] = 'http://127.0.0.1:8000'

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

class ChannelData:
    direct = 0
    organic = 0
    organic_conversion = 0
    organic_conversion_rate = 0
    paid = 0
    referral = 0
    display = 0
    social = 0
    email = 0
    others = 0

    def set(self, channel, amount, cv):
        if channel == 'Direct':
            self.direct += amount
        elif channel == 'Organic Search':
            self.organic += amount
            self.organic_conversion += cv
            self.organic_conversion_rate = percentage(cv, amount)
        elif channel == 'Paid Search':
            self.paid += amount
        elif channel == 'Referral':
            self.referral += amount
        elif channel == 'Display':
            self.display += amount
        elif channel == 'Social':
            self.social += amount
        elif channel == 'Email':
            self.email += amount
        elif channel == '(Other)':
            self.others += amount

    def get(self, channel):
        if channel == 'direct':
            return self.direct
        elif channel == 'organic':
            return self.organic
        elif channel == 'organic_conversion':
            return self.organic_conversion
        elif channel == 'organic_conversion_rate':
            return self.organic_conversion_rate
        elif channel == 'paid':
            return self.paid
        elif channel == 'referral':
            return self.referral
        elif channel == 'display':
            return self.display
        elif channel == 'social':
            return self.social
        elif channel == 'email':
            return self.email
        elif channel == 'others':
            return self.others

def get_results(service, profile_id, start, end, term):
    data = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start,
            end_date=end,
            metrics='ga:users,ga:sessions,ga:pageviews,ga:goalCompletionsAll',
            dimensions=f'ga:{term},ga:channelGrouping',
            sort='ga:' + term
            ).execute().get('rows')
    channel = {}
    for d in data:
        if d[0] not in channel:
            channel[d[0]] = ChannelData()
        channel[d[0]].set(d[1], int(d[3]), int(d[5]))
    data = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start,
            end_date=end,
            metrics='ga:users,ga:sessions,ga:pageviews,ga:goalCompletionsAll',
            dimensions=f'ga:{term}',
            sort='ga:' + term,
            ).execute().get('rows')
    output = []
    for d in data:
        if term == 'yearWeek':
            date = datetime.strptime(f'{d[0]}-7', '%Y%U-%u')
        elif term == 'yearMonth':
            date = datetime.strptime(f'{d[0]}', '%Y%m')
        item = {
            'date': date,
            'users': d[1],
            'session': d[2],
            'pv': d[3],
            'cv': d[4],
            'cvr': percentage(d[4], d[2]),
            'pvr': percentage(d[3], d[2]),
        }
        if d[0] in channel:
            item['direct'] = channel[d[0]].get('direct')
            item['organic'] = channel[d[0]].get('organic')
            item['organic_conversion'] = channel[d[0]].get('organic_conversion')
            item['organic_conversion_rate'] = channel[d[0]].get('organic_conversion_rate')
            item['paid'] = channel[d[0]].get('paid')
            item['referral'] = channel[d[0]].get('referral')
            item['display'] = channel[d[0]].get('display')
            item['social'] = channel[d[0]].get('social')
            item['email'] = channel[d[0]].get('email')
            item['others'] = channel[d[0]].get('others')
        else:
            item['direct'] = 0
            item['organic'] = 0
            item['organic_conversion'] = 0
            item['organic_conversion_rate'] = 0.0
            item['paid'] = 0
            item['referral'] = 0
            item['display'] = 0
            item['social'] = 0
            item['email'] = 0
            item['others'] = 0
        output.append(item)
    return output

def percentage(part, whole):
    if whole == '0':
        return 0.0
    percentage = 100 * float(part)/float(whole)
    return round(percentage, 1)

def get_all_analytics_data(start, end, term, account_info):
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = f'{os.environ["CP_CONFIG_PATH"]}column-port-service.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    #status_code = validate_account_info(service, account_info)
    #if not status_code == 0:
    #    return status_code
    return get_results(service, account_info[2], start, end, term)

def get_weekly_analytics_data(week, account_info):
    week = week - 1
    day = date.today() - timedelta(days=7)
    yr = day.strftime('%Y')
    wk = day.strftime('%U')

    end_day = datetime.strptime(f'{yr}-{wk}-6', '%Y-%U-%u')
    start_day = end_day - timedelta(days=6+(week*7))
    end = end_day.strftime('%Y-%m-%d')
    start = start_day.strftime('%Y-%m-%d')

    return get_all_analytics_data(start, end, "yearWeek", account_info)

def get_monthly_analytics_data(month, account_info):
    day = date.today() - relativedelta(months=1)
    past = day.today() - relativedelta(months=month)

    end_day = day.replace(day=calendar.monthrange(day.year, day.month)[1])
    start_day = past.replace(day=1)
    end = end_day.strftime('%Y-%m-%d')
    start = start_day.strftime('%Y-%m-%d')

    return get_all_analytics_data(start, end, "yearMonth", account_info)

#if __name__ == '__main__':