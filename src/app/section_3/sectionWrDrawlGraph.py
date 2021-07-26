import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as mdates


def fetchWrDrawlGraphContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> bool:
    mRepo = MetricsDataRepo(appDbConnStr)

    # get iex rtm data for the range between start date and end date
    wbesRtmIexVals = mRepo.getWbesRtmIexBeneficiaryBlockWiseData(startDt, endDt,beneficiary='West ',beneficiary_type=' Drawal ')

    wbesRtmPxiVals = mRepo.getWbesRtmPxiBeneficiaryBlockWiseData(startDt, endDt,beneficiary='West ',beneficiary_type=' Drawal ')
    wbesPxIexVals = mRepo.getWbesPxIexBeneficiaryBlockWiseData(startDt, endDt,beneficiary='West ',beneficiary_type=' Drawal ')

    wbesPxPxiVals = mRepo.getWbesPxPxiBeneficiaryBlockWiseData(startDt, endDt,beneficiary='West ',beneficiary_type=' Drawal ')

    wbesRtmIexDf = pd.DataFrame(wbesRtmIexVals)
    wbesRtmPxiDf = pd.DataFrame(wbesRtmPxiVals)
    wbesPxIexDf = pd.DataFrame(wbesPxIexVals)
    wbesPxPxiDf = pd.DataFrame(wbesPxPxiVals)

    # wbesRtmPxiDf['date']=wbesRtmPxiDf['time_stamp'].dt.date
    # wbesRtmPxiDf['time']=wbesRtmPxiDf['time_stamp'].dt.time
    wbesRtmPxiDf.drop(['beneficiary','beneficiary_type'],axis=1,inplace=True)
    # wbesRtmPxiDf = wbesRtmPxiDf.pivot(index='time',columns='date', values='data_value')


    # wbesRtmIexDf['date'] = wbesRtmIexDf['time_stamp'].dt.date
    # wbesRtmIexDf['time'] = wbesRtmIexDf['time_stamp'].dt.time
    wbesRtmIexDf.drop(['beneficiary', 'beneficiary_type'], axis=1, inplace=True)
    # wbesRtmIexDf = wbesRtmIexDf.pivot(index='time', columns='date', values='data_value')
    wbesPxIexDf.drop(['beneficiary','beneficiary_type'],axis=1,inplace=True)
    wbesPxPxiDf.drop(['beneficiary','beneficiary_type'],axis=1,inplace=True)
    wbesPxDf = wbesRtmPxiDf.append(wbesPxIexDf,ignore_index=False).groupby(['time_stamp']).sum().reset_index()
    wbesRtmDf = wbesRtmPxiDf.append(wbesRtmIexDf,ignore_index=False).groupby(['time_stamp']).sum().reset_index()
    wbesRtmDf['time_stamp']=wbesRtmDf['time_stamp'].dt.date
    wbesPxDf['time_stamp']=wbesPxDf['time_stamp'].dt.date

    wbesRtmDfMax = wbesRtmDf.groupby(['time_stamp']).max().reset_index()
    wbesRtmDfMin = wbesRtmDf.groupby(['time_stamp']).min().reset_index()
    mergewbesRtmDf=pd.merge(wbesRtmDfMax,wbesRtmDfMin,on='time_stamp')
    mergewbesRtmDf.set_index(['time_stamp'],inplace=True)
    mergewbesRtmDf = mergewbesRtmDf.rename(columns={'data_value_x': 'RTM_MAX','data_value_y':'RTM_MIN'})

    wbesPxDfMax = wbesPxDf.groupby(['time_stamp']).max().reset_index()
    wbesPxDfMin = wbesPxDf.groupby(['time_stamp']).min().reset_index()
    mergeWbesPxDf=pd.merge(wbesPxDfMax,wbesPxDfMin,on='time_stamp')
    mergeWbesPxDf.set_index(['time_stamp'],inplace=True)
    mergeWbesPxDf = mergeWbesPxDf.rename(columns={'data_value_x': 'DAM_MAX','data_value_y':'DAM_MIN'})

    # derive plot title
    pltTitle = 'WR Buy RTM vs DAM'

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # instantiate a second axes that shares the same x-axis
    ax2 = ax.twinx()
    # set plot title
    ax.set_title(pltTitle)
    ax.set_ylabel('MW')
    ax2.set_ylabel('RTM BUY MIN(MW)')
    ax.set_facecolor("#474747")
    # fig.patch.set_facecolor('#d9ccff')

    clr = ['#66b3ff', '#df80ff', '#ff6666', '#00b359']

    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(
        mergewbesRtmDf.index.values, mergewbesRtmDf['RTM_MAX'].values, color='#66b3ff')
    laThisMonth.set_label('RTM Buy Max')

    laLastYear, = ax.plot(
        mergeWbesPxDf.index.values, mergeWbesPxDf['DAM_MAX'].values, color='#df80ff')
    laLastYear.set_label('DAM Buy Max')

    laPrevMonth, = ax2.plot(
        mergewbesRtmDf.index.values, mergewbesRtmDf['RTM_MIN'].values, color='#00b359')
    laPrevMonth.set_label('RTM Buy Min')

    laPrevMonth, = ax.plot(
        mergeWbesPxDf.index.values, mergeWbesPxDf['DAM_MIN'].values, color='#ff6666')
    laPrevMonth.set_label('DAM Buy Min')
    # plt.show()
    # ax.set_xlim((1, 31), auto=True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='best',
              ncol=3, mode="expand", borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower right',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_3_2.png')

    plt.close()


    return True
