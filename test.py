# import argparse
import datetime as dt

# generate report word file monthly_rep_template
tmplPath: str = "templates/monthly_rep_template.docx"

# create weekly report
endDt = dt.datetime.now() - dt.timedelta(days=1)
endDt = dt.datetime(endDt.year,endDt.month,endDt.day)
startDt = endDt - dt.timedelta(days=5)
endDt = endDt + dt.timedelta(hours=23, minutes=59)
print('Report generation Done')
