from src.typeDefs.wbesPxTableRecord import ISection_2_2, IWbesPxHeaders, IWbesPxTableRecord
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd


def fetchWbesPxTableContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_2_2:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex Px data for the range between start date and end date
    wbesPxIexVals = mRepo.getWbesPxIexBlockWiseData(startDt, endDt)
    wbesPxPxiVals = mRepo.getWbesPxPxiBlockWiseData(startDt, endDt)
    wbesPxIexDf = pd.DataFrame(wbesPxIexVals)
    wbesPxPxiDf = pd.DataFrame(wbesPxPxiVals)

    wbesPxIexTableDf = wbesPxIexDf.groupby(['time_stamp', 'beneficiary', 'beneficiary_type']).sum()
    wbesPxPxiTableDf = wbesPxPxiDf.groupby(['time_stamp', 'beneficiary', 'beneficiary_type']).sum()
    wbesPxIexTableDf = wbesPxIexTableDf.rename(columns={'data_value': 'px_iex_data'})
    wbesPxIexTableDf.reset_index(inplace = True)
    index_names = wbesPxIexTableDf[wbesPxIexTableDf['beneficiary_type'] == 'path'].index
    wbesPxIexTableDf.drop(index_names, inplace = True)
    index_names = wbesPxIexTableDf[wbesPxIexTableDf['beneficiary'] == 'West '].index
    wbesPxIexTableDf.drop(index_names, inplace = True)
    wbesPxIexTableDf.reset_index(inplace = True)
    for itr in range(len(wbesPxIexTableDf)):
        if wbesPxIexTableDf['beneficiary_type'][itr] == ' Injection ':
            wbesPxIexTableDf['beneficiary_type'][itr] = 'Sell'
            wbesPxIexTableDf['px_iex_data'][itr] = -1*(wbesPxIexTableDf['px_iex_data'][itr])
        if wbesPxIexTableDf['beneficiary_type'][itr] == ' Drawal ':
            wbesPxIexTableDf['beneficiary_type'][itr] = 'Buy'
    wbesPxIexTableDf['beneficiary_name'] = wbesPxIexTableDf.beneficiary.str.cat(wbesPxIexTableDf.beneficiary_type,sep=" ")
    wbesPxIexTableDf.drop(['index', 'beneficiary_type', 'beneficiary'],axis=1,inplace=True)

    wbesPxPxiTableDf = wbesPxPxiTableDf.rename(columns={'data_value': 'px_pxi_data'})
    wbesPxPxiTableDf.reset_index(inplace = True)
    index_names = wbesPxPxiTableDf[wbesPxPxiTableDf['beneficiary_type'] == 'path'].index
    wbesPxPxiTableDf.drop(index_names, inplace = True)
    index_names = wbesPxPxiTableDf[wbesPxPxiTableDf['beneficiary'] == 'West '].index
    wbesPxPxiTableDf.drop(index_names, inplace = True)
    wbesPxPxiTableDf.reset_index(inplace = True)
    for itr in range(len(wbesPxPxiTableDf)):
        if wbesPxPxiTableDf['beneficiary_type'][itr] == ' Injection ':
            wbesPxPxiTableDf['beneficiary_type'][itr] = 'Sell'
            wbesPxPxiTableDf['px_pxi_data'][itr] = -1*(wbesPxPxiTableDf['px_pxi_data'][itr])
        if wbesPxPxiTableDf['beneficiary_type'][itr] == ' Drawal ':
            wbesPxPxiTableDf['beneficiary_type'][itr] = 'Buy'
    wbesPxPxiTableDf['beneficiary_name'] = wbesPxPxiTableDf.beneficiary.str.cat(wbesPxPxiTableDf.beneficiary_type,sep=" ")
    wbesPxPxiTableDf.drop(['index', 'beneficiary_type', 'beneficiary'],axis=1,inplace=True)

    # testing 
    testPxIex = wbesPxIexTableDf 
    testPxPxi = wbesPxPxiTableDf 
    testPxPxi = testPxPxi.rename(columns={'px_pxi_data': 'data_value'})
    testPxIex = testPxIex.rename(columns={'px_iex_data': 'data_value'})
    testPxIex = testPxIex.append(testPxPxi, ignore_index=True)
    testPxIex = testPxIex.groupby(['time_stamp', 'beneficiary_name']).sum()
    testPxIex.reset_index(inplace = True)
    testPxIex['data_value'] = testPxIex['data_value']/4
    testPxIex['data_value'] = testPxIex['data_value'].astype(int)
    testPxIex['time_stamp'] = pd.to_datetime(testPxIex['time_stamp']).dt.date
    # testPxIex['time_stamp'] = testPxIex['time_stamp'].dt.strftime('%d-%m-%Y')
    testPxIex = testPxIex.pivot(
        index='beneficiary_name', columns='time_stamp', values='data_value')
    testPxIex = testPxIex.fillna(0)
    testPxPxi = testPxPxi.rename(columns={'data_value': 'wbes_rtm_data'})
    wbesPxTableDf = testPxIex
    wbesPxTableDf['Grand Total'] = wbesPxTableDf.sum(axis=1)
    index_names = wbesPxTableDf[wbesPxTableDf['Grand Total'] == 0].index
    wbesPxTableDf.drop(index_names, inplace = True)

    # testing starts
    wbesPxTableDf.reset_index(inplace = True)
    injection_vals = wbesPxTableDf[wbesPxTableDf['Grand Total'] < 0].index
    injection_df = wbesPxTableDf.loc[injection_vals]
    injection_sum = injection_df.select_dtypes(pd.np.number).sum().rename('total')
    drawal_vals = wbesPxTableDf[wbesPxTableDf['Grand Total'] > 0].index
    drawal_df = wbesPxTableDf.loc[drawal_vals]
    drawal_sum = drawal_df.select_dtypes(pd.np.number).sum().rename('total')
    # testing ends

    wbesPxTableDf.reset_index(inplace = True)
    wbesPxTableDf = wbesPxTableDf.sort_values(by='Grand Total')

    # demo starts
    wbesPxTableDf= wbesPxTableDf.append(injection_sum,ignore_index=True)
    for itr in range(len(wbesPxTableDf['beneficiary_name'])):
        if(pd.isnull(wbesPxTableDf['beneficiary_name'][itr])):
            wbesPxTableDf['beneficiary_name'][itr] = 'Total WR Sell'
            wbesPxTableDf['Grand Total'][itr] = sum(injection_sum)/2
    wbesPxTableDf= wbesPxTableDf.append(drawal_sum,ignore_index=True)
    for itr in range(len(wbesPxTableDf['beneficiary_name'])):
        if(pd.isnull(wbesPxTableDf['beneficiary_name'][itr])):
            wbesPxTableDf['beneficiary_name'][itr] = 'Total WR Buy'
            wbesPxTableDf['Grand Total'][itr] = sum(drawal_sum)/2

    # del wbesPxTableDf['Grand Total']      
    # wbesPxTableDf.drop(['Grand Total'],axis=1,inplace=True)
    # wbesPxTableDf['Grand Total'] = wbesPxTableDf.sum(axis=1)
    # demo starts

    wbesPxTableDf.reset_index(inplace = True)
    wbesPxTableDf.drop(['index', 'level_0'],axis=1,inplace=True)

    px_headers = []
    i= 0
    cols = []
    for itr in wbesPxTableDf.columns:
        cols.append(itr)
        if itr == 'beneficiary_name':
            temp = {
                'day_{0}'.format(i):'Px Traded Energy(MWH)'
            }
            i+=1
            px_headers.append(temp)
        elif itr == 'Grand Total':
            temp = {
                'tot'.format(i):'Grand Total'
            }
            i+=1
            px_headers.append(temp)
        else:
            temp = {
                'day_{0}'.format(i): itr
            }
            i+=1
            px_headers.append(temp)

    WbesPxTableList: ISection_2_2["wbes_px_table"] = []

    for i in wbesPxTableDf.index:
        wbesPxDailyRecord: IWbesPxTableRecord = {
            'ben_name': wbesPxTableDf[cols[0]][i],
            'day_1': round(wbesPxTableDf[cols[1]][i]),
            'day_2': round(wbesPxTableDf[cols[2]][i]),
            'day_3': round(wbesPxTableDf[cols[3]][i]),
            'day_4': round(wbesPxTableDf[cols[4]][i]),
            'day_5': round(wbesPxTableDf[cols[5]][i]),
            'day_6': round(wbesPxTableDf[cols[6]][i]),
            'day_7': round(wbesPxTableDf[cols[7]][i]),
            'tot': round(wbesPxTableDf[cols[8]][i])
        }
        WbesPxTableList.append(wbesPxDailyRecord)
    secData: ISection_2_2 = {
        'px_headers': px_headers,
        'wbes_px_table': WbesPxTableList
    }
    
    return secData
