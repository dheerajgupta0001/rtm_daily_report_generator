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
            wbesRtmIexTableDf['beneficiary_type'][itr] = 'Sell'
            wbesRtmIexTableDf['rtm_iex_data'][itr] = -1*(wbesRtmIexTableDf['rtm_iex_data'][itr])
        if wbesRtmIexTableDf['beneficiary_type'][itr] == ' Drawal ':
            wbesRtmIexTableDf['beneficiary_type'][itr] = 'Buy'
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
            wbesRtmPxiTableDf['beneficiary_type'][itr] = 'Sell'
            wbesRtmPxiTableDf['rtm_pxi_data'][itr] = -1*(wbesRtmPxiTableDf['rtm_pxi_data'][itr])
        if wbesRtmPxiTableDf['beneficiary_type'][itr] == ' Drawal ':
            wbesRtmPxiTableDf['beneficiary_type'][itr] = 'Buy'
    wbesRtmPxiTableDf['beneficiary_name'] = wbesRtmPxiTableDf.beneficiary.str.cat(wbesRtmPxiTableDf.beneficiary_type,sep=" ")
    wbesRtmPxiTableDf.drop(['index', 'beneficiary_type', 'beneficiary'],axis=1,inplace=True)

    # testing 
    testRtmIex = wbesRtmIexTableDf 
    testRtmPxi = wbesRtmPxiTableDf 
    testRtmPxi = testRtmPxi.rename(columns={'rtm_pxi_data': 'data_value'})
    testRtmIex = testRtmIex.rename(columns={'rtm_iex_data': 'data_value'})
    testRtmIex = testRtmIex.append(testRtmPxi, ignore_index=True)
    testRtmIex = testRtmIex.groupby(['time_stamp', 'beneficiary_name']).sum()
    testRtmIex.reset_index(inplace = True)
    testRtmIex['data_value'] = testRtmIex['data_value']/4
    testRtmIex['data_value'] = testRtmIex['data_value'].astype(int)
    # testRtmIex['time_stamp'] = pd.to_datetime(testRtmIex['time_stamp'], format='%d-%m-%Y')
    testRtmIex['time_stamp'] = testRtmIex['time_stamp'].dt.strftime('%d-%m-%Y')
    testRtmIex = testRtmIex.pivot(
        index='beneficiary_name', columns='time_stamp', values='data_value')
    testRtmIex = testRtmIex.fillna(0)
    testRtmPxi = testRtmPxi.rename(columns={'data_value': 'wbes_rtm_data'})
    wbesRtmTableDf = testRtmIex
    wbesRtmTableDf['Grand Total'] = wbesRtmTableDf.sum(axis=1)
    index_names = wbesRtmTableDf[wbesRtmTableDf['Grand Total'] == 0].index
    wbesRtmTableDf.drop(index_names, inplace = True)

    # testing starts
    wbesRtmTableDf.reset_index(inplace = True)
    injection_vals = wbesRtmTableDf[wbesRtmTableDf['Grand Total'] < 0].index
    injection_df = wbesRtmTableDf.loc[injection_vals]
    injection_sum = injection_df.select_dtypes(pd.np.number).sum().rename('total')
    drawal_vals = wbesRtmTableDf[wbesRtmTableDf['Grand Total'] > 0].index
    drawal_df = wbesRtmTableDf.loc[drawal_vals]
    drawal_sum = drawal_df.select_dtypes(pd.np.number).sum().rename('total')
    # testing ends

    wbesRtmTableDf.reset_index(inplace = True)
    wbesRtmTableDf = wbesRtmTableDf.sort_values(by='Grand Total')

    # demo starts
    wbesRtmTableDf= wbesRtmTableDf.append(injection_sum,ignore_index=True)
    for itr in range(len(wbesRtmTableDf['beneficiary_name'])):
        if(pd.isnull(wbesRtmTableDf['beneficiary_name'][itr])):
            wbesRtmTableDf['beneficiary_name'][itr] = 'Total WR Sell'
            wbesRtmTableDf['Grand Total'][itr] = sum(injection_sum)/2
    wbesRtmTableDf= wbesRtmTableDf.append(drawal_sum,ignore_index=True)
    for itr in range(len(wbesRtmTableDf['beneficiary_name'])):
        if(pd.isnull(wbesRtmTableDf['beneficiary_name'][itr])):
            wbesRtmTableDf['beneficiary_name'][itr] = 'Total WR Buy'
            wbesRtmTableDf['Grand Total'][itr] = sum(drawal_sum)/2
            
    # demo starts

    wbesRtmTableDf.reset_index(inplace = True)
    wbesRtmTableDf.drop(['index', 'level_0'],axis=1,inplace=True)

    headers = []
    i= 0
    cols = []
    for itr in wbesRtmTableDf.columns:
        cols.append(itr)
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

    WbesRtmTableList: ISection_2_1["wbes_rtm_table"] = []

    for i in wbesRtmTableDf.index:
        wbesRtmDailyRecord: IWbesRtmTableRecord = {
            'ben_name': wbesRtmTableDf[cols[0]][i],
            'day_1': round(wbesRtmTableDf[cols[1]][i]),
            'day_2': round(wbesRtmTableDf[cols[2]][i]),
            'day_3': round(wbesRtmTableDf[cols[3]][i]),
            'day_4': round(wbesRtmTableDf[cols[4]][i]),
            'day_5': round(wbesRtmTableDf[cols[5]][i]),
            'day_6': round(wbesRtmTableDf[cols[6]][i]),
            'day_7': round(wbesRtmTableDf[cols[7]][i]),
            'tot': round(wbesRtmTableDf[cols[8]][i])
        }
        WbesRtmTableList.append(wbesRtmDailyRecord)
    secData: ISection_2_1 = {
        'headers': headers,
        'wbes_rtm_table': WbesRtmTableList
    }
    
    return secData
