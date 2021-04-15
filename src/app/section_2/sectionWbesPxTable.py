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
            wbesPxIexTableDf['px_iex_data'][itr] = -1*(wbesPxIexTableDf['px_iex_data'][itr])
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
            wbesPxPxiTableDf['px_pxi_data'][itr] = -1*(wbesPxPxiTableDf['px_pxi_data'][itr])
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
    testPxIex['time_stamp'] = testPxIex['time_stamp'].dt.strftime('%d-%m-%Y')
    testPxIex = testPxIex.pivot(
        index='beneficiary_name', columns='time_stamp', values='data_value')
    testPxIex = testPxIex.fillna(0)
    testPxPxi = testPxPxi.rename(columns={'data_value': 'wbes_rtm_data'})
    wbesPxTableDf = testPxIex
    wbesPxTableDf['Grand Total'] = wbesPxTableDf.sum(axis=1)
    index_names = wbesPxTableDf[wbesPxTableDf['Grand Total'] == 0].index
    wbesPxTableDf.drop(index_names, inplace = True)
    wbesPxTableDf.reset_index(inplace = True)
    wbesPxTableDf = wbesPxTableDf.sort_values(by='Grand Total')
    wbesPxTableDf.reset_index(inplace = True)
    wbesPxTableDf.drop(['index'],axis=1,inplace=True)

    # wbesPxTableDf = wbesPxIexTableDf.merge(wbesPxPxiTableDf[['time_stamp', 'beneficiary_name', 'px_pxi_data']])
    # wbesPxTableDf['wbes_rtm_data'] = (wbesPxTableDf['px_iex_data'] + wbesPxTableDf['px_pxi_data'])/4
    # wbesPxTableDf['wbes_rtm_data'] = wbesPxTableDf['wbes_rtm_data'].astype(int)
    # wbesPxTableDf.drop(['px_iex_data', 'px_pxi_data'],axis=1,inplace=True)
    # wbesPxTableDf['time_stamp'] = wbesPxTableDf['time_stamp'].dt.strftime('%d-%m-%Y')
    # wbesPxTableDf = wbesPxTableDf.pivot(
    #     index='beneficiary_name', columns='time_stamp', values='wbes_rtm_data')
    # wbesPxTableDf['Grand Total'] = wbesPxTableDf.sum(axis=1)
    # index_names = wbesPxTableDf[wbesPxTableDf['Grand Total'] == 0].index
    # wbesPxTableDf.drop(index_names, inplace = True)
    # wbesPxTableDf.reset_index(inplace = True)
    # wbesPxTableDf = wbesPxTableDf.sort_values(by='Grand Total')

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
    # cols[0] = 'beneficiary_name'
    # cols.append('Grand Total')
    # rowSumList = wbesPxTableDf.sum(axis=0)

    WbesPxTableList: ISection_2_1["wbes_rtm_table"] = []

    for i in wbesPxTableDf.index:
        wbesPxDailyRecord: IWbesPxTableRecord = {
            # 'ben_name': wbesPxTableDf['beneficiary_name'][i],
            # 'day_1': wbesPxTableDf['04-04-2021'][i],
            # 'day_2': wbesPxTableDf['05-04-2021'][i],
            # 'day_3': wbesPxTableDf['04-04-2021'][i],
            # 'day_4': wbesPxTableDf['05-04-2021'][i],
            # 'day_5': wbesPxTableDf['04-04-2021'][i],
            # 'day_6': wbesPxTableDf['05-04-2021'][i],
            # 'day_7': wbesPxTableDf['04-04-2021'][i],
            # 'tot': wbesPxTableDf['Grand Total'][i]
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
