import pandas as pd
from functions import get_time_series, get_daily_reports, get_date_list

confirmed, deaths, recovered = get_time_series(local=True)
daily_report_data, dates = get_daily_reports(local=True)

date_list = get_date_list(dates)

totals_by_day = pd.DataFrame(
    data={
        'confirmed': [confirmed[date].sum() for date in date_list],
        'deaths': [deaths[date].sum() for date in date_list],
        'recovered': [recovered[date].sum() for date in date_list]
    }, index=date_list)

