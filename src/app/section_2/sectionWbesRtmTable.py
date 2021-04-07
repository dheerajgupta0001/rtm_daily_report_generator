from src.typeDefs.wbesRtmTableRecord import ISection_2_1, IWbesRtmHeaders, IWbesRtmTableRecord
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd


def fetchWbesRtmTableContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_2_1:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex rtm data for the range between start date and end date
    wbesRtmIexVals = mRepo.getWbesRtmIexBlockWiseData(startDt, endDt)
    wbesRtmPxiVals = mRepo.getWbesRtmPxiBlockWiseData(startDt, endDt)
    wbesRtmIexDf = pd.DataFrame(wbesRtmIexVals)
    wbesRtmPxiDf = pd.DataFrame(wbesRtmPxiVals)

    wbesRtmIexTableDf = wbesRtmIexDf.groupby(['time_stamp', 'beneficiary', 'beneficiary_type']).sum()
    wbesRtmPxiTableDf = wbesRtmPxiDf.groupby(['time_stamp', 'beneficiary', 'beneficiary_type']).sum()
    wbesRtmIexTableDf = wbesRtmIexTableDf.rename(columns={'data_value': 'rtm_iex_data'})
    wbesRtmIexTableDf.reset_index(inplace = True)
    index_names = wbesRtmIexTableDf[wbesRtmIexTableDf['beneficiary_type'] == 'path'].index
    wbesRtmIexTableDf.drop(index_names, inplace = True)
    index_names = wbesRtmIexTableDf[wbesRtmIexTableDf['beneficiary'] == 'West '].index
    wbesRtmIexTableDf.drop(index_names, inplace = True)
    wbesRtmIexTableDf.reset_index(inplace = True)
    for itr in range(len(wbesRtmIexTableDf)):
        if wbesRtmIexTableDf['beneficiary_type'][itr] == ' Injection ':
            wbesRtmIexTableDf['rtm_iex_data'][itr] = -1*(wbesRtmIexTableDf['rtm_iex_data'][itr])
    wbesRtmIexTableDf['beneficiary_name'] = wbesRtmIexTableDf.beneficiary.str.cat(wbesRtmIexTableDf.beneficiary_type,sep=" ")
    wbesRtmIexTableDf.drop(['index', 'beneficiary_type', 'beneficiary'],axis=1,inplace=True)

    wbesRtmPxiTableDf = wbesRtmPxiTableDf.rename(columns={'data_value': 'rtm_pxi_data'})
    wbesRtmPxiTableDf.reset_index(inplace = True)
    index_names = wbesRtmPxiTableDf[wbesRtmPxiTableDf['beneficiary_type'] == 'path'].index
    wbesRtmPxiTableDf.drop(index_names, inplace = True)
    index_names = wbesRtmPxiTableDf[wbesRtmPxiTableDf['beneficiary'] == 'West '].index
    wbesRtmPxiTableDf.drop(index_names, inplace = True)
    wbesRtmPxiTableDf.reset_index(inplace = True)
    for itr in range(len(wbesRtmPxiTableDf)):
        if wbesRtmPxiTableDf['beneficiary_type'][itr] == ' Injection ':
            wbesRtmPxiTableDf['rtm_pxi_data'][itr] = -1*(wbesRtmPxiTableDf['rtm_pxi_data'][itr])
    wbesRtmPxiTableDf['beneficiary_name'] = wbesRtmPxiTableDf.beneficiary.str.cat(wbesRtmPxiTableDf.beneficiary_type,sep=" ")
    wbesRtmPxiTableDf.drop(['index', 'beneficiary_type', 'beneficiary'],axis=1,inplace=True)

    wbesRtmTableDf = wbesRtmIexTableDf.merge(wbesRtmPxiTableDf[['time_stamp', 'beneficiary_name', 'rtm_pxi_data']])
    wbesRtmTableDf['wbes_rtm_data'] = (wbesRtmTableDf['rtm_iex_data'] + wbesRtmTableDf['rtm_pxi_data'])/4
    wbesRtmTableDf['wbes_rtm_data'] = wbesRtmTableDf['wbes_rtm_data'].astype(int)
    wbesRtmTableDf.drop(['rtm_iex_data', 'rtm_pxi_data'],axis=1,inplace=True)
    wbesRtmTableDf['time_stamp'] = wbesRtmTableDf['time_stamp'].dt.strftime('%d-%m-%Y')
    wbesRtmTableDf = wbesRtmTableDf.pivot(
        index='beneficiary_name', columns='time_stamp', values='wbes_rtm_data')
    wbesRtmTableDf['Grand Total'] = wbesRtmTableDf.sum(axis=1)
    index_names = wbesRtmTableDf[wbesRtmTableDf['Grand Total'] == 0].index
    wbesRtmTableDf.drop(index_names, inplace = True)
    wbesRtmTableDf.reset_index(inplace = True)
    wbesRtmTableDf = wbesRtmTableDf.sort_values(by='Grand Total')

    headers = []
    i= 0
    for itr in wbesRtmTableDf.columns:
        if itr == 'beneficiary_name':
            temp = {
                'day_{0}'.format(i):'RTM Traded Energy(MWH)'
            }
            i+=1
            headers.append(temp)
        elif itr == 'Grand Total':
            temp = {
                'tot'.format(i):'Grand Total'
            }
            i+=1
            headers.append(temp)
        else:
            temp = {
                'day_{0}'.format(i): itr
            }
            i+=1
            headers.append(temp)

    # rowSumList = wbesRtmTableDf.sum(axis=0)

    WbesRtmTableList: ISection_2_1["wbes_rtm_table"] = []

    for i in wbesRtmTableDf.index:
        wbesRtmDailyRecord: IWbesRtmTableRecord = {
            'ben_name': wbesRtmTableDf['beneficiary_name'][i],
            'day_1': wbesRtmTableDf['04-04-2021'][i],
            'day_2': wbesRtmTableDf['05-04-2021'][i],
            'day_3': wbesRtmTableDf['04-04-2021'][i],
            'day_4': wbesRtmTableDf['05-04-2021'][i],
            'day_5': wbesRtmTableDf['04-04-2021'][i],
            'day_6': wbesRtmTableDf['05-04-2021'][i],
            'day_7': wbesRtmTableDf['04-04-2021'][i],
            'tot': wbesRtmTableDf['Grand Total'][i]
        }
        WbesRtmTableList.append(wbesRtmDailyRecord)
    secData: ISection_2_1 = {
        'headers': headers,
        'wbes_rtm_table': WbesRtmTableList
    }
    
    return secData