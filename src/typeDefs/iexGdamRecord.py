from typing import TypedDict, List
import datetime as dt

class IIexGdamRecord(TypedDict):
    date_time: dt.datetime
    min_mcv: float
    max_mcv: float
    avg_mcv: float
    min_mcp: float
    max_mcp: float
    avg_mcp: float
    rtm_energy: float

class ISection_1_4(TypedDict):
    iex_gdam_table: List[IIexGdamRecord]
    # reportDt: dt.datetime