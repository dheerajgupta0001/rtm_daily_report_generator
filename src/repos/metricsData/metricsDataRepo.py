from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord
from src.repos.getIexRtmBlockWiseData import getIexRtmBlockWiseData
from src.repos.getIexDamBlockWiseData import getIexDamBlockWiseData
from src.repos.getWbesRtmIexBlockWiseData import getWbesRtmIexBlockWiseData
from src.repos.getWbesRtmPxiBlockWiseData import getWbesRtmPxiBlockWiseData
from src.repos.getWbesPxPxiBlockWiseData import getWbesPxPxiBlockWiseData
from src.repos.getWbesPxIexBlockWiseData import getWbesPxIexBlockWiseData


class MetricsDataRepo():
    """Repository class for entity metrics data
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr

    def getIexRtmBlockWiseData(self, col_attributes: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getIexRtmBlockWiseData(appDbConnStr=self.appDbConnStr, col_attributes=col_attributes, startDt=startDt, endDt=endDt)

    def getIexDamBlockWiseData(self, col_attributes: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getIexDamBlockWiseData(appDbConnStr=self.appDbConnStr, col_attributes=col_attributes, startDt=startDt, endDt=endDt)

    def getWbesRtmIexBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesRtmIexBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)

    def getWbesRtmPxiBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesRtmPxiBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)

    def getWbesPxIexBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesPxIexBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)

    def getWbesPxPxiBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesPxPxiBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)
