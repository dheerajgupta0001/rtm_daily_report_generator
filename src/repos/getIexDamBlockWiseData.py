import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IMetricsDataRecord


def getIexDamBlockWiseData(appDbConnStr: str, col_attributes: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
    targetColumns = ['TRUNC(TIME_STAMP)', 'COL_ATTRIBUTES', 'DATA_VALUE']

    metricsFetchSql = """

            select {0} from 
            mo_warehouse.iex_dam where time_stamp >= :1
            and time_stamp < :2
            and col_attributes = :3
        """.format(','.join(targetColumns), col_attributes)

    # initialise codes to be returned
    dataRecords: List[IMetricsDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (startDt, endDt, col_attributes))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching iex dam data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []

    # iterate through each row to populate result outage rows
    for row in dbRows:
        timeStamp: IMetricsDataRecord["time_stamp"] = row[colNames.index(
            'TRUNC(TIME_STAMP)')]
        metric: IMetricsDataRecord["col_attributes"] = row[colNames.index(
            'COL_ATTRIBUTES')]
        val: IMetricsDataRecord["data_value"] = row[colNames.index(
            'DATA_VALUE')]
        sampl: IMetricsDataRecord = {
            "time_stamp": timeStamp,
            "metric_name": metric,
            "data_value": val
        }
        dataRecords.append(sampl)
    return dataRecords
