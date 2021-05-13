from src.typeDefs.iexGtamDerivedRecord import IIexGtamDerivedDataRecord, ISection_4_1
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
import numpy as np


def fetchIexGtamDerivedTable(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_4_1:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex rtm data for the range between start date and end date
    endDt = endDt - dt.timedelta(days=1)
    tradeDt = endDt
    iexGtamDerivedVals = mRepo.getIexGtamDerivedData(tradeDt)
    tableDf = pd.DataFrame(iexGtamDerivedVals)

    summ = tableDf.select_dtypes(pd.np.number).sum().rename('total')
    tableDf= tableDf.append(summ,ignore_index=True)

    productType = []
    for itr in range(len(tableDf['contract_type'])):
        if(tableDf['contract_type'][itr] == 'DAC'):
            productType.append("DAC")
            tableDf['contract_type'][itr] = 'TOTAL'
        if(tableDf['contract_type'][itr] == 'DAC-NS'):
            productType.append("DAC")
            tableDf['contract_type'][itr] = '   NS'
        if(tableDf['contract_type'][itr] == 'DAC-SL'):
            productType.append("DAC")
            tableDf['contract_type'][itr] = '   SL'
        
        if(tableDf['contract_type'][itr] == 'DYL'):
            productType.append("DAILY(DYL)")
            tableDf['contract_type'][itr] = 'TOTAL'
        if(tableDf['contract_type'][itr] == 'DYL-SL'):
            productType.append("DAILY")
            tableDf['contract_type'][itr] = '   SL'
        if(tableDf['contract_type'][itr] == 'DYL-NS'):
            productType.append("DAILY")
            tableDf['contract_type'][itr] = '   NS'

        if(tableDf['contract_type'][itr] == 'FDL'):
            productType.append("DAILY(FDL)")
            tableDf['contract_type'][itr] = 'TOTAL'
        if(tableDf['contract_type'][itr] == 'FDL-SL'):
            productType.append("DAILY")
            tableDf['contract_type'][itr] = '   SL'
        if(tableDf['contract_type'][itr] == 'FDL-NS'):
            productType.append("DAILY")
            tableDf['contract_type'][itr] = '   NS'

        if(tableDf['contract_type'][itr] == 'ITD'):
            productType.append("INTRADAY")
            tableDf['contract_type'][itr] = 'TOTAL'
        if(tableDf['contract_type'][itr] == 'ITD-NS'):
            productType.append("INTRADAY")
            tableDf['contract_type'][itr] = '   NS'
        if(tableDf['contract_type'][itr] == 'ITD-SL'):
            productType.append("INTRADAY")
            tableDf['contract_type'][itr] = '   SL'

        if(tableDf['contract_type'][itr] == 'WEK'):
            productType.append("WEEKLY")
            tableDf['contract_type'][itr] = 'TOTAL'
        if(tableDf['contract_type'][itr] == 'WEK-SL'):
            productType.append("WEEKLY")
            tableDf['contract_type'][itr] = '   SL'
        if(tableDf['contract_type'][itr] == 'WEK-NS'):
            productType.append("WEEKLY")
            tableDf['contract_type'][itr] = '   NS'

        if(pd.isnull(tableDf['contract_type'][itr])):
            productType.append(" ")
            tableDf['contract_type'][itr] = 'GRAND TOTAL'

    iexGtamDerivedTableList: ISection_4_1["iex_gtam_derived_table"] = []
    tableDf['product_type'] = productType

    for i in tableDf.index:
        iexGtamDerivedRecord: IIexGtamDerivedDataRecord = {
            'product_type': tableDf['product_type'][i],
            'contract_type': tableDf['contract_type'][i],
            'highest_price': round(tableDf['highest_price'][i]),
            'lowest_price': round(tableDf['lowest_price'][i]),
            'max_trades': round(tableDf['max_trades'][i]),
            'total_trades': round(tableDf['total_trades'][i]),
            'total_traded_vol': round(tableDf['total_traded_vol'][i])
        }
        iexGtamDerivedTableList.append(iexGtamDerivedRecord)
    tradeDt = dt.datetime(endDt.year, endDt.month, endDt.day)
    tradeDt = dt.datetime.strftime(tradeDt, '%d-%m-%Y')
    secData: ISection_4_1 = {
        'iex_gtam_derived_table': iexGtamDerivedTableList,
        'tradeDt': tradeDt
    }
    
    return secData
