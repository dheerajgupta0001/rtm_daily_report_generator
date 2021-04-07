from src.typeDefs.iexRtmRecord import IIexRtmRecord, ISection_1_1
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd


def fetchIexRtmTableContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> IIexRtmRecord:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex rtm data for the range between start date and end date
    iexRtmMcvVals = mRepo.getIexRtmBlockWiseData('MCV (MW)', startDt, endDt)
    iexRtmMcpVals = mRepo.getIexRtmBlockWiseData('MCP (Rs/MWh) ', startDt, endDt)
    iexRtmMcvDf = pd.DataFrame(iexRtmMcvVals)
    iexRtmMcpDf = pd.DataFrame(iexRtmMcpVals)

    tableDf = iexRtmMcvDf.groupby(['time_stamp']).mean()
    tableDf = tableDf.rename(columns={'data_value': 'avg_mcv_data'})
    tableDf.reset_index(inplace = True)
    minDf = iexRtmMcvDf.groupby(['time_stamp']).min()
    minDf.reset_index(inplace = True)
    minDf = minDf.rename(columns={'data_value': 'min_mcv_data'})
    tableDf = tableDf.merge(minDf[['min_mcv_data', 'time_stamp']], on = 'time_stamp')
    maxDf = iexRtmMcvDf.groupby(['time_stamp']).max()
    maxDf = maxDf.rename(columns={'data_value': 'max_mcv_data'})
    maxDf.reset_index(inplace = True)
    tableDf = tableDf.merge(maxDf[['max_mcv_data', 'time_stamp']], on = 'time_stamp')

    minMcpDf = iexRtmMcpDf.groupby(['time_stamp']).min()
    minMcpDf.reset_index(inplace = True)
    minMcpDf = minMcpDf.rename(columns={'data_value': 'min_mcp_data'})
    minMcpDf['min_mcp_data'] = minMcpDf['min_mcp_data']/1000
    tableDf = tableDf.merge(minMcpDf[['min_mcp_data', 'time_stamp']], on = 'time_stamp')
    maxMcpDf = iexRtmMcpDf.groupby(['time_stamp']).max()
    maxMcpDf.reset_index(inplace = True)
    maxMcpDf = maxMcpDf.rename(columns={'data_value': 'max_mcp_data'})
    maxMcpDf['max_mcp_data'] = maxMcpDf['max_mcp_data']/1000
    tableDf = tableDf.merge(maxMcpDf[['max_mcp_data', 'time_stamp']], on = 'time_stamp')
    avgMcpDf = iexRtmMcpDf.groupby(['time_stamp']).mean()
    avgMcpDf.reset_index(inplace = True)
    avgMcpDf = avgMcpDf.rename(columns={'data_value': 'avg_mcp_data'})
    avgMcpDf['avg_mcp_data'] = avgMcpDf['avg_mcp_data']/1000
    tableDf = tableDf.merge(avgMcpDf[['avg_mcp_data', 'time_stamp']], on = 'time_stamp')
    tableDf['rtm_energy'] = tableDf['avg_mcv_data']*24/1000


    iexRtmTableList: ISection_1_1["iex_rtm_table"] = []

    for i in tableDf.index:
        iexRtmDailyRecord: IIexRtmRecord = {
            'date_time': dt.datetime.strftime(tableDf['time_stamp'][i], '%d-%m-%Y'),
            'min_mcv': round(tableDf['min_mcv_data'][i]),
            'max_mcv': round(tableDf['max_mcv_data'][i]),
            'avg_mcv': round(tableDf['avg_mcv_data'][i]),
            'min_mcp': round(tableDf['min_mcp_data'][i], 1),
            'max_mcp': round(tableDf['max_mcp_data'][i], 1),
            'avg_mcp': round(tableDf['avg_mcp_data'][i], 1),
            'rtm_energy': round(tableDf['rtm_energy'][i])
        }
        iexRtmTableList.append(iexRtmDailyRecord)
    reportDt = dt.datetime(endDt.year, endDt.month, endDt.day)
    reportDt = dt.datetime.strftime(reportDt, '%Y-%m-%d')
    secData: IIexRtmRecord = {
        'iex_rtm_table': iexRtmTableList,
        'reportDt': reportDt
    }
    
    return secData
