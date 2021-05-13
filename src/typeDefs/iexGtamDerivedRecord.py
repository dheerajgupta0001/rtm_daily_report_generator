from typing import TypedDict, List
import datetime as dt


class IIexGtamDerivedDataRecord(TypedDict):
    # time_stamp: dt.datetime
    product_type: str
    contract_type: str
    highest_price: float
    lowest_price: float
    max_trades: float
    total_trades: float
    total_traded_vol: float

class ISection_4_1(TypedDict):
    iex_gtam_derived_table: List[IIexGtamDerivedDataRecord]
    tradeDt: dt.datetime