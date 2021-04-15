from typing import TypedDict, List
import datetime as dt

class IWbesPxHeaders(TypedDict):
    day_0: str
    day_1: float
    day_2: float
    day_3: float
    day_4: float
    day_5: float
    day_6: float
    day_7: float
    tot: float

class IWbesPxTableRecord(TypedDict):
    ben_name: str
    day_1: float
    day_2: float
    day_3: float
    day_4: float
    day_5: float
    day_6: float
    day_7: float
    tot: float

class ISection_2_2(TypedDict):
    wbes_px_table: List[IWbesPxTableRecord]
    px_headers: List[IWbesPxHeaders]