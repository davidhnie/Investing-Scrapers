
#Author: David Nie 
#call with "python <prgm name> <date in format m/d/Y> <date in format m/d/Y>
#Anaconda --> cd C:\Users\Dima\Anaconda2\envs\py35
#(C:\Users\Dima\Anaconda2) C:\Users\Dima\Anaconda2\envs\py35>python D:\Safe_IKF\IKF_DimaN\Projects\Web_data_scrapers\scraper_NASDAQ_earn.py 07/10/2017 07/14/2017

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import sys
from datetime import datetime, timedelta, date

nasdaq = "http://www.nasdaq.com/earnings/earnings-calendar.aspx?date="

today = datetime.combine(date.today(), datetime.min.time())
#call with command line 
s1= sys.argv[1]
s2= sys.argv[2]
date = datetime.strptime(s1, "%m/%d/%Y")
end = datetime.strptime(s2, "%m/%d/%Y")
start = date

#data contains all ticker and date info 
data = [["Company Name", "Company Name (Symbol)", "Market Cap", "Event_type","Time",
"Report Date", "Report Date (Euro)", "Fiscal Quarter Ending", 
"Consensus EPS Forecast","# of Ests","Last Year's Report Date", "Last Year's EPS",
"EPS", "% Surprise"]]

while date<=end:
    
    page = urllib.request.urlopen(nasdaq+str(date.year)+'-'+str(date.month)+'-'+str(date.day))
    soup = bs.BeautifulSoup(page,'html.parser')

    #correctly id tables
    tables = soup.find_all('table',{'class':'USMN_EarningsCalendar'})

    #find rows with information and create list 
    try:
        #CONFIRMED DATA
        rows=tables[0].find_all('tr')[1:]
        
        for i in range(len(rows)):

            companyName = re.findall('">.*?[(]', str(rows[i]))[-1][2:-2]
            companyName = re.sub(r'&amp;', r'&', companyName) #subs
            companyName = re.sub(r';', r'', companyName)

            companySymbol = re.findall('[(].*?[)]', str(rows[i]))[-1][1:-1]
            cap = re.findall('Market Cap:.*</', str(rows[i]))[-1][12:-6] 
            try:
                time = re.findall('title=".*?">',str(rows[i].find_all('td')[0]))[0][7:-3] 
            except IndexError:
                time = "n/a"
            reportDate = re.findall('../../....',str(rows[i].find_all('td')[2]))[0]
            date = datetime.strptime(reportDate, "%m/%d/%Y")
            euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year) 
            fiscalQ = re.findall('\t[A-Za-z0-9 ]*\r',str(rows[i].find_all('td')[3]))[0][5:-1]
            consensusEPS = re.findall('\$[0-9\.-]*',str(rows[i].find_all('td')[4]))[0]
            estimateNum = re.findall('[0-9]+',str(rows[i].find_all('td')[5]))[0]


            #dates before today
            if date < today:
                lastYearDate = "n/a"
                lastYearEPS = "n/a"
                try:
                    EPS = re.findall('\$[0-9\.-]*',str(rows[i].find_all('td')[7]))[0]
                except IndexError:
                    EPS = "n/a"
                surprise = max(re.findall('[0-9.-]*',str(rows[i].find_all('td')[8])), key=len)
                if surprise == '':
                    surprise = "n/a"

            #could use: more secure::: rows[i].find_all('td')[#####].string.split()[0]
            #dates after today
            else:
                EPS = "n/a"
                surprise = "n/a"
                try:
                    lastYearDate = re.findall('../../....',str(rows[i].find_all('td')[6]))[0]
                except IndexError:
                    lastYearDate = "n/a"
                try:
                    lastYearEPS = re.findall('\$[0-9\.-]*',str(rows[i].find_all('td')[7]))[0]
                except IndexError:
                    lastYearEPS = "n/a"

            cols = [companyName,
            companySymbol,
            cap,
            "Confirmed",
            time,
            reportDate,
            euroDate,
            fiscalQ,
            consensusEPS,
            estimateNum,
            lastYearDate,
            lastYearEPS,
            EPS,
            surprise
            ]
            data.append(cols)

    except IndexError:
        print("No available data for confirmed on " + date.strftime('%m-%d-%Y'))
        

    try:

        #ESTIMATED DATA
        rows=tables[1].find_all('tr')[1:]
    

        for i in range(len(rows)):

            companyName = re.findall('">.*?[(]', str(rows[i]))[-1][2:-2]
            companyName = re.sub(r'&amp;', r'&', companyName)
            companyName = re.sub(r';', r'', companyName)
            
            companySymbol = re.findall('[(].*?[)]', str(rows[i]))[-1][1:-1]  
            cap = re.findall('Market Cap:.*</', str(rows[i]))[-1][12:-6] 
            reportDate = re.findall('../../....',str(rows[i].find_all('td')[1]))[0]
            date = datetime.strptime(reportDate, "%m/%d/%Y")
            euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
            fiscalQ = re.findall('\t[A-Za-z0-9 ]*\r',str(rows[i].find_all('td')[2]))[0][5:-1]
            consensusEPS = re.findall('\$[0-9\.-]*',str(rows[i].find_all('td')[3]))[0]
            estimateNum = re.findall('[0-9]+',str(rows[i].find_all('td')[4]))[0]
            

            try:
                lastYearDate = re.findall('../../....',str(rows[i].find_all('td')[5]))[0]
            except IndexError:
                lastYearDate = "n/a"

            try:
                lastYearEPS = re.findall('\$[0-9\.-]*',str(rows[i].find_all('td')[6]))[0]
            except IndexError:
                lastYearEPS = "n/a"

            cols = [companyName,
            companySymbol,
            cap,
            "Estimated",
            "n/a",
            reportDate,
            euroDate,
            fiscalQ,
            consensusEPS,
            estimateNum,
            lastYearDate,
            lastYearEPS,
            "n/a",
            "n/a"
            ]
            data.append(cols)

    except IndexError:
        print("No available data for estimated on " + date.strftime('%m-%d-%Y'))

    #set date 
    date = date + timedelta(days=1)

#write data to csv
with open ('D:\\Safe_IKF\\IKF_DimaN\\Projects\\Web_data_scrapers\\Output_files\\NADSAQ-earn-'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)
