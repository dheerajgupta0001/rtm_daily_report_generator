import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IWbesMetricsDataRecord


def getWbesPxPxiBeneficiaryBlockWiseData(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime,beneficiary:str,beneficiary_type:str) -> List[IWbesMetricsDataRecord]:
    targetColumns = ['TIME_STAMP', 'BENEFICIARY' ,'DATA_VALUE', 'BENEFICIARY_TYPE']

    metricsFetchSql = """
            select {0} from 
            mo_warehouse.WBES_Px_PXI sf
            where sf.TIME_STAMP >= :1 and sf.TIME_STAMP < :2 
            and sf.BENEFICIARY = :3
            and sf.BENEFICIARY_TYPE = :4
            order by sf.TIME_STAMP asc
            """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IWbesMetricsDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (startDt, endDt,beneficiary,beneficiary_type))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching wbes rtm iex data between dates')
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
        timeStamp: IWbesMetricsDataRecord["time_stamp"] = row[colNames.index(
            'TIME_STAMP')]
        benef_Name: IWbesMetricsDataRecord["col_attributes"] = row[colNames.index(
            'BENEFICIARY')]
        val: IWbesMetricsDataRecord["data_value"] = row[colNames.index(
            'DATA_VALUE')]
        benef_type: IWbesMetricsDataRecord["beneficiary_type"] = row[colNames.index(
            'BENEFICIARY_TYPE')]
        sampl: IWbesMetricsDataRecord = {
            "time_stamp": timeStamp,
            "beneficiary": benef_Name,
            "data_value": val,
            "beneficiary_type": benef_type
        }
        dataRecords.append(sampl)
    return dataRecords
