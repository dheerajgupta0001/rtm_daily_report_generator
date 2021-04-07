# import argparse
import datetime as dt
from src.config.appConfig import getJsonConfig, initConfigs
from src.app.rtmReportGenerator import RtmDailyReportGenerator

initConfigs()

# get app config
appConfig = getJsonConfig()

# get app db connection string from config file
appDbConStr: str = appConfig['appDbConnStr']
dumpFolder: str = appConfig['dumpFolder']

# generate report word file monthly_rep_template
tmplPath: str = "templates/rtm_report_template.docx"

# create weekly report
rtmRprtGntr = RtmDailyReportGenerator(appDbConStr)
# endDt = dt.datetime.now() - dt.timedelta(days=13)
endDt = dt.datetime.now()
endDt = dt.datetime(endDt.year,endDt.month,endDt.day)
startDt = endDt - dt.timedelta(days=8)
endDt = endDt + dt.timedelta(days=1)
rtmRprtGntr.generateRtmDailyReport(startDt, endDt, tmplPath, dumpFolder)
print('Report generation Done')