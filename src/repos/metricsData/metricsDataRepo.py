from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord
from src.repos.getIexRtmBlockWiseData import getIexRtmBlockWiseData
from src.repos.getIexDamBlockWiseData import getIexDamBlockWiseData
# from src.typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord
from src.repos.getWbesRtmIexBlockWiseData import getWbesRtmIexBlockWiseData
from src.repos.getWbesRtmPxiBlockWiseData import getWbesRtmPxiBlockWiseData
from src.repos.getWbesRtmIexBeneficiaryBlockWiseData import getWbesRtmIexBeneficiaryBlockWiseData
from src.repos.getWbesRtmPxiBeneficiaryBlockWiseData import getWbesRtmPxiBeneficiaryBlockWiseData
from src.repos.getWbesPxPxiBeneficiaryBlockWiseData import getWbesPxPxiBeneficiaryBlockWiseData
from src.repos.getWbesPxIexBeneficiaryBlockWiseData import getWbesPxIexBeneficiaryBlockWiseData





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

    def getWbesRtmIexBeneficiaryBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime,beneficiary:str,beneficiary_type:str) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesRtmIexBeneficiaryBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt,beneficiary=beneficiary,beneficiary_type=beneficiary_type)

    def getWbesRtmPxiBeneficiaryBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime,beneficiary:str,beneficiary_type:str) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesRtmPxiBeneficiaryBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt,beneficiary=beneficiary,beneficiary_type=beneficiary_type)

    def getWbesPxPxiBeneficiaryBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime,beneficiary:str,beneficiary_type:str) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesPxPxiBeneficiaryBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt,beneficiary=beneficiary,beneficiary_type=beneficiary_type)

    def getWbesPxIexBeneficiaryBlockWiseData(self, startDt: dt.datetime, endDt: dt.datetime,beneficiary:str,beneficiary_type:str) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getWbesPxIexBeneficiaryBlockWiseData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt,beneficiary=beneficiary,beneficiary_type=beneficiary_type)
