import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as mdates


def fetchIexGraphContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> bool:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex rtm data for the range between start date and end date
    startDt = endDt - dt.timedelta(days=1)
    iexDamMcvVals = mRepo.getIexDamBlockWiseData('MCV (MW)', startDt, endDt)
    iexDamMcpVals = mRepo.getIexDamBlockWiseData('MCP (Rs/MWh) ', startDt, endDt)
    for itr in range(len(iexDamMcvVals)):
        iexDamMcvVals[itr]['metric_name'] = 'DAM MCV(MW)'
        iexDamMcvVals[itr]['time_stamp'] = itr+1
    for itr in range(len(iexDamMcpVals)):
        iexDamMcpVals[itr]['metric_name'] = 'DAM MCP(Rs/KWH)'
        iexDamMcpVals[itr]['time_stamp'] = itr+1
    iexRtmMcvVals = mRepo.getIexRtmBlockWiseData('MCV (MW)', startDt, endDt)
    iexRtmMcpVals = mRepo.getIexRtmBlockWiseData('MCP (Rs/MWh) ', startDt, endDt)
    for itr in range(len(iexRtmMcvVals)):
        iexRtmMcvVals[itr]['metric_name'] = 'RTM MCV(MW)'
        iexRtmMcvVals[itr]['time_stamp'] = itr+1
    for itr in range(len(iexRtmMcpVals)):
        iexRtmMcpVals[itr]['metric_name'] = 'RTM MCP(Rs/KWH)'
        iexRtmMcpVals[itr]['time_stamp'] = itr+1

    # create plot image for demands of prev yr, prev month, this month
    iexDamMcvObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexDamMcvVals]
    iexDamMcpObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexDamMcpVals]
    iexRtmMcvObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexRtmMcvVals]
    iexRtmMcpObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexRtmMcpVals]
    pltDataObjs = iexDamMcvObjs + iexDamMcpObjs + iexRtmMcvObjs + iexRtmMcpObjs
    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='Date', columns='colName', values='val')
    pltDataDf['DAM MCP(Rs/KWH)'] = pltDataDf['DAM MCP(Rs/KWH)']/1000
    pltDataDf['RTM MCP(Rs/KWH)'] = pltDataDf['RTM MCP(Rs/KWH)']/1000

    # derive plot title
    pltTitle = 'MCP & MCV Data as per IEX Data'
    dateStr = startDt.strftime("%d-%m-%Y")
    pltTitle = 'MCP & MCV Data as per IEX Data for {0}'.format(dateStr)

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # instantiate a second axes that shares the same x-axis
    ax2 = ax.twinx()
    # set plot title
    ax.set_title(pltTitle)
    # set y labels
    ax2.set_ylabel('Rs/KWH')
    ax.set_ylabel('MWH')
    ax.set_facecolor("#474747")

    # set y axis limit
    # fig.patch.set_facecolor('#d9ccff')

    clr = ['#66b3ff', '#df80ff', '#ff6666', '#00b359']
    # set x xis manually
    x_test = [1,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96]

    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf['DAM MCV(MW)'].values, color='#66b3ff')
    laThisMonth.set_label('DAM MCV(MW)')

    laLastYear, = ax2.plot(
        pltDataDf.index.values, pltDataDf['DAM MCP(Rs/KWH)'].values, color='#df80ff')
    laLastYear.set_label('DAM MCP(Rs/KWH)')

    laPrevMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf['RTM MCV(MW)'].values, color='#00b359')
    laPrevMonth.set_label('RTM MCV(MW)')

    laPrevMonth, = ax2.plot(
        pltDataDf.index.values, pltDataDf['RTM MCP(Rs/KWH)'].values, color='#ff6666')
    laPrevMonth.set_label('RTM MCP(Rs/KWH)')

    ax.set_xlim((1,96), auto = True)
    ax.set_xticks([1,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96])
    # ax.set_xlim((1, 31), auto=True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='best',
              ncol=3, mode="expand", borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower right',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_3.png')
    plt.close()

    return True
