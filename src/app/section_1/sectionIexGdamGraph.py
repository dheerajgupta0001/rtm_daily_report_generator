import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as mdates


def fetchIexGdamGraphContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> bool:
    mRepo = MetricsDataRepo(appDbConnStr)
    
    # get iex rtm data for the range between start date and end date
    startDt = endDt - dt.timedelta(days=1)
    iexGdamMcvVals = mRepo.getIexGdamBlockWiseData('MCV (MW)', startDt, endDt)
    iexGdamMcpVals = mRepo.getIexGdamBlockWiseData('MCP (Rs/MWh) ', startDt, endDt)
    for itr in range(len(iexGdamMcvVals)):
        iexGdamMcvVals[itr]['metric_name'] = 'GDAM MCV(MW)'
        iexGdamMcvVals[itr]['time_stamp'] = itr+1
    for itr in range(len(iexGdamMcpVals)):
        iexGdamMcpVals[itr]['metric_name'] = 'GDAM MCP(Rs/KWH)'
        iexGdamMcpVals[itr]['time_stamp'] = itr+1

    # create plot image for demands of prev yr, prev month, this month
    iexGdamMcvObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexGdamMcvVals]
    iexGdamMcpObjs = [{'Date': 
        x["time_stamp"], 'colName': x['metric_name'], 'val': x["data_value"]} for x in iexGdamMcpVals]
    
    pltDataObjs = iexGdamMcvObjs + iexGdamMcpObjs
    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='Date', columns='colName', values='val')
    pltDataDf['GDAM MCP(Rs/KWH)'] = pltDataDf['GDAM MCP(Rs/KWH)']/1000

    # derive plot title
    # pltTitle = 'GDAM MCP & MCV Data as per IEX Data'
    dateStr = startDt.strftime("%d-%m-%Y")
    pltTitle = 'GDAM MCP & MCV Data as per IEX Data for {0}'.format(dateStr)

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
        pltDataDf.index.values, pltDataDf['GDAM MCV(MW)'].values, color='#66b3ff')
    laThisMonth.set_label('GDAM MCV(MW)')

    laLastYear, = ax2.plot(
        pltDataDf.index.values, pltDataDf['GDAM MCP(Rs/KWH)'].values, color='#df80ff')
    laLastYear.set_label('GDAM MCP(Rs/KWH)')


    ax.set_xlim((1,96), auto = True)
    ax.set_xticks([1,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96])
    # ax.set_xlim((1, 31), auto=True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='best',
              ncol=3, mode="expand", borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower right',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_3_b.png')
    plt.close()

    return True
