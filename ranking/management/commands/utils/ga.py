from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'column-port-d779fd6160a5.json'

def sample_run_report(property_id="276819055"): #←プロパティID
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",  #←プロパティID
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="2022-03-26", end_date="today")],
    )
    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)

if __name__ == '__main__':
    sample_run_report()