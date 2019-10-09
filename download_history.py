import datetime
import requests
import time
import pandas as pd
import os

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def get_info():
    results_per_req = 750
    session = requests.Session()
    url = 'https://www.bitmex.com/api/v1/trade/bucketed'

    oldest_date_time = datetime.datetime.now()
    now_date_time = datetime.datetime.now()
    desired_delta = datetime.timedelta(days=365)

    req_n = 0

    while now_date_time - oldest_date_time < desired_delta:
        data_set = []
        req_params = {
            'count': results_per_req,
            'binSize': '5m',
            'partial': 'false',
            'symbol': 'XBTUSD',
            'reverse': 'true',
            'start': req_n * results_per_req,
        }

        response = session.get(url, params=req_params)
        req_n += 1

        # TODO check symbol and distribute stocks to diff files
        response_json = response.json()
        for line in response_json:
            data_set.append(line)
        data_set_list = []
        for singleEntry in data_set:
            # TODO check which columns you need - (currently) timestamp/symbol/close
            # row = [singleEntry.get("timestamp"), singleEntry.get("symbol"), singleEntry.get("open"),
            #        singleEntry.get("high"),
            #        singleEntry.get("low"), singleEntry.get("close"), singleEntry.get("trades"),
            #        singleEntry.get("volume"),
            #        singleEntry.get("vwap"), singleEntry.get("lastSize"), singleEntry.get("turnover"),
            #        singleEntry.get("homeNotional"), singleEntry.get("foreighNotional")]
            row = [singleEntry.get("timestamp"), singleEntry.get("symbol"), singleEntry.get("close")]
            data_set_list.append(row)
        df = pd.DataFrame(data_set_list)
        if not os.path.isfile('XBTUSD.csv'):
            df.to_csv('XBTUSD.csv', header='column_names', index=False)
        else:
            df.to_csv('XBTUSD.csv', mode='a', header=False, index=False)

        oldest = response.json()[-1]['timestamp']
        oldest_date_time = datetime.datetime.strptime(oldest, DATE_TIME_FORMAT)
        print(req_n, oldest_date_time)

        reset = int(response.headers['X-RateLimit-Reset'])
        rem = int(response.headers['X-RateLimit-Remaining'])

        if not rem:
            now = int(time.time())
            wait_time = reset - now
            if wait_time > 0:
                print('sleep to reset: ', wait_time)
                time.sleep(wait_time)


get_info()
