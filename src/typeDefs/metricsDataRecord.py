from typing import TypedDict
import datetime as dt


class IMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    col_attributes: str
    data_value: float

class IWbesMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    beneficiary: str
    data_value: float
    beneficiary_type: float