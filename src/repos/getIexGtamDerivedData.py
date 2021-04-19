import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.iexGtamDerivedRecord import IIexGtamDerivedDataRecord


def getIexGtamDerivedData(appDbConnStr: str, tradeDt: dt.datetime) -> List[IIexGtamDerivedDataRecord]:
    targetColumns = ['TIME_STAMP', 'CONTRACT_TYPE', 'HIGHEST_PRICE',
                     'LOWEST_PRICE', 'MAX_TRADES', 'TOTAL_TRADES', 'TOTAL_TRADED_VOL']

    metricsFetchSql = """

            select {0} from 
            mo_warehouse.IEX_GTAM_DERIVE where time_stamp = :1
            and time_stamp = :2
        """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IIexGtamDerivedDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (tradeDt, tradeDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching iex gtam derived data between dates')
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
        timeStamp: IIexGtamDerivedDataRecord["time_stamp"] = row[colNames.index(
            'TIME_STAMP')]
        contract_type: IIexGtamDerivedDataRecord["contract_type"] = row[colNames.index(
            'CONTRACT_TYPE')]
        highest_price: IIexGtamDerivedDataRecord["highest_price"] = row[colNames.index(
            'HIGHEST_PRICE')]
        lowest_price: IIexGtamDerivedDataRecord["lowest_price"] = row[colNames.index(
            'LOWEST_PRICE')]
        max_trades: IIexGtamDerivedDataRecord["max_trades"] = row[colNames.index(
            'MAX_TRADES')]
        total_trades: IIexGtamDerivedDataRecord["total_trades"] = row[colNames.index(
            'TOTAL_TRADES')]
        total_traded_vol: IIexGtamDerivedDataRecord["total_traded_vol"] = row[colNames.index(
            'TOTAL_TRADED_VOL')]
        sampl: IIexGtamDerivedDataRecord = {
            "contract_type": contract_type,
            "highest_price": highest_price,
            "lowest_price": lowest_price,
            "max_trades": max_trades,
            "total_trades": total_trades,
            "total_traded_vol": total_traded_vol
        }
        dataRecords.append(sampl)
    return dataRecords
