import os
import datetime as dt
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
from src.app.section_1.sectionIexRtmTable import fetchIexRtmTableContext
from src.app.section_1.sectionIexDamTable import fetchIexDamTableContext
from src.app.section_1.sectionIexGraph import fetchIexGraphContext
from src.typeDefs.iexRtmRecord import IIexRtmRecord
from src.app.section_2.sectionWbesRtmTable import fetchWbesRtmTableContext
from src.app.section_3.sectionWrInjGraph import fetchWrInjGraphContext
from src.app.section_3.sectionWrDrawlGraph import fetchWrDrawlGraphContext


from src.app.section_2.sectionWbesPxTable import fetchWbesPxTableContext
# from docx2pdf import convert


class RtmDailyReportGenerator:
    appDbConStr: str = ''

    sectionCtrls = {
        '1_1': True,
        '1_2': True,
        '1_3': True,
        '2_1': True,
        '2_2':True,
        '3_1':True,
        '3_2':True
    }

    def __init__(self, appDbConStr: str, secCtrls: dict = {}):
        self.appDbConStr = appDbConStr
        self.sectionCtrls.update(secCtrls)

    def getReportContextObj(self, startDt: dt.datetime, endDt: dt.datetime) -> IReportCxt:
        """get the report context object for populating the weekly report template
        Args:
            monthDt (dt.datetime): month date object
        Returns:
            IReportCxt: report context object
        """
        # create context for weekly report
        reportContext: IReportCxt = {}

        if self.sectionCtrls["1_1"]:
            # get section 1.1 data
            try:
                secIexRtmData = fetchIexRtmTableContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secIexRtmData)
                print(
                    "section iex rtm table context setting complete")
            except Exception as err:
                print(
                    "error while fetching section iex rtm table")
                print(err)

        if self.sectionCtrls["1_2"]:
            # get section 1.2 data
            try:
                secIexDamData = fetchIexDamTableContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secIexDamData)
                print(
                    "section iex dam table context setting complete")
            except Exception as err:
                print(
                    "error while fetching section iex dam table")
                print(err)

        if self.sectionCtrls["1_3"]:
            # get section 1.3 data
            try:
                secIexGraphData = fetchIexGraphContext(
                    self.appDbConStr, startDt, endDt)
                # reportContext.update(secIexGraphData)
                print(
                    "section iex dam rtm graph plotting done")
            except Exception as err:
                print(
                    "error while iex dam rtm graph plotting")
                print(err)

        if self.sectionCtrls["2_1"]:
            # get section 2.1 data
            try:
                secWbesRtmData = fetchWbesRtmTableContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secWbesRtmData)
                print(
                    "section wbes rtm table context setting complete")
            except Exception as err:
                print(
                    "error while fetching section wbes rtm table")
                print(err)

        if self.sectionCtrls["3_1"]:
            # get section 3.1 data
            try:
                secWrInjGraph = fetchWrInjGraphContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secWrInjGraph)
                print(
                    "section wr injection graph context setting complete")
            except Exception as err:
                print(
                    "error while fetching section wr injection graph")
                print(err)

        if self.sectionCtrls["3_2"]:
            # get section 3.1 data
            try:
                secWrDrawlGraph = fetchWrDrawlGraphContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secWrDrawlGraph)
                print(
                    "section wr drawal graph context setting complete")
            except Exception as err:
                print(
                    "error while fetching section wr drawal graph")
                print(err)


        if self.sectionCtrls["2_2"]:
            # get section 2.1 data
            try:
                secWbesRtmData = fetchWbesPxTableContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secWbesRtmData)
                print(
                    "section wbes px table context setting complete")
            except Exception as err:
                print(
                    "error while fetching section wbes px table")
                print(err)

        return reportContext

    def generateReportWithContext(self, reportContext: IReportCxt, tmplPath: str, dumpFolder: str, endDt: dt.datetime) -> bool:
        """generate the report file at the desired dump folder location
        based on the template file and report context object
        Args:
            reportContext (IReportCxt): report context object
            tmplPath (str): full file path of the template
            dumpFolder (str): folder path for dumping the generated report
        Returns:
            bool: True if process is success, else False
        """
        try:
            doc = DocxTemplate(tmplPath)
            # populate section 1.4.2 plot image in word file
            if self.sectionCtrls["1_3"]:
                plot_1_3_path = 'assets/section_1_3.png'
                plot_1_3_img = InlineImage(doc, plot_1_3_path)
                reportContext['plot_1_3'] = plot_1_3_img

            
            doc.render(reportContext)

            # derive document path and save
            dumpFileName = 'Rtm_Report_{0}.docx'.format(
                reportContext['reportDt'])
            dumpFileFullPath = os.path.join(dumpFolder, dumpFileName)
            doc.save(dumpFileFullPath)
        except Exception as err:
            print("error while saving monthly report from context for month ")
            print(err)
            return False
        return True

    def generateRtmDailyReport(self, startDt: dt.datetime, endDt: dt.datetime, tmplPath: str, dumpFolder: str) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file
        Args:
            startDt (dt.datetime): start date
            tmplPath (str): full file path of the template file
            dumpFolder (str): folder path where the generated reports are to be dumped
        Returns:
            bool: True if process is success, else False
        """
        reportCtxt = self.getReportContextObj(startDt, endDt)
        isSuccess = self.generateReportWithContext(
            reportCtxt, tmplPath, dumpFolder, endDt)
        # convert report to pdf
        # convert(dumpFileFullPath, dumpFileFullPath.replace('.docx', '.pdf'))
        return isSuccess
