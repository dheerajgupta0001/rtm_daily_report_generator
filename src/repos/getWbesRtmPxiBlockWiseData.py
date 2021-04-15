import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IWbesMetricsDataRecord


def getWbesRtmPxiBlockWiseData(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IWbesMetricsDataRecord]:
    targetColumns = ['TRUNC(TIME_STAMP)', 'BENEFICIARY' ,'DATA_VALUE', 'BENEFICIARY_TYPE']

    metricsFetchSql = """
            select {0} from 
            mo_warehouse.WBES_RTM_PXI where time_stamp >= :1
            and time_stamp < :2
            order by time_stamp asc
        """.format(','.join(targetColumns))

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
        dbCur.execute(metricsFetchSql, (startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching wbes rtm pxi data between dates')
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
        beneficiary: IMetricsDataRecord["col_attributes"] = row[colNames.index(
            'BENEFICIARY')]
        val: IMetricsDataRecord["data_value"] = row[colNames.index(
            'DATA_VALUE')]
        beneficiary_type: IMetricsDataRecord["data_value"] = row[colNames.index(
            'BENEFICIARY_TYPE')]
        sampl: IWbesMetricsDataRecord = {
            "time_stamp": timeStamp,
            "beneficiary": beneficiary,
            "data_value": val,
            "beneficiary_type": beneficiary_type
        }
        dataRecords.append(sampl)
    return dataRecords
