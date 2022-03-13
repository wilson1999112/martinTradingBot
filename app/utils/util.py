import os
import pandas as pd
header_list = [
    "Date","Open","High","Low","Close","Volume",
    "Close time","Quote asset volume","Number of trades",
    "Taker buy base asset volume","Taker buy quote asset volume","Ignore"]
need_list = ["Open","High","Low","Close","Volume"]
def _date_converter(s):
    return pd.to_datetime(s, unit='ms')

def _read_file(filename):
    return pd.read_csv(filename, converters={0:_date_converter},
                       index_col=0, parse_dates=True, infer_datetime_format=True,
                       names=header_list)[need_list]

def _filename_loader(dir):
    for (dirPath, _, fileNames) in os.walk(dir):
        for fileName in fileNames:
            yield os.path.join(dirPath, fileName)

def data_loader(dir):
    df_list = []
    for filename in _filename_loader(dir):
        df_list.append(_read_file(filename))
    return pd.concat(df_list)