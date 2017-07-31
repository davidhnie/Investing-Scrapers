
#Author: David Nie 
#call with "python <prgm name> <date in format m/d/Y> <date in format m/d/Y>
#Anaconda --> cd C:\Users\Dima\Anaconda2\envs\py35
#(C:\Users\Dima\Anaconda2) C:\Users\Dima\Anaconda2\envs\py35>python D:\Safe_IKF\IKF_DimaN\Projects\Web_data_scrapers\scraper_NASDAQ_div.py 07/10/2017 07/14/2017

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import sys
from datetime import datetime, timedelta


nasdaq = "http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date="

#call with command line 
s1= sys.argv[1]#"07/07/2017"#sys.argv[1]
s2= sys.argv[2]#"07/17/2017"#sys.argv[2]
date = datetime.strptime(s1, "%m/%d/%Y")
end = datetime.strptime(s2, "%m/%d/%Y")
start = date

#data contains all the tickers and dates
data = [["Company Name", "Company (Symbol)","Event_type","Ex-Dividend Date","Ex-Dividend Date (Euro)", "Dividend",
"Indicated Annual Dividend","Record Date","Announcement Date","Payment Date"]]

while date<=end :
    
    page = urllib.request.urlopen(nasdaq+str(date.year)+'-'+str(date.month)+'-'+str(date.day))
    #page = urllib.urlopen(nasdaq+str(date.year)+'-'+str(date.month)+'-'+str(date.day))
    soup = bs.BeautifulSoup(page,'html.parser')

    #correctly id the table
    table = soup.find('table',{'id':'Table1'})

    # HANDLE NON-AVAILABE TRADE DAYS . . . . . 
    try:
        table_body=table.find('tbody')
        rows = table_body.find_all('tr')
        for i in range(len(rows)):
            company = re.findall('>.*\xa0', str(rows[i].td.a))[-1][1:-1]
            company = re.sub(r'&amp;', r'&', company)
            company = re.sub(r';', r'', company)

            symbol = re.findall('[(].*?[)]', str(rows[i].td.a))[-1][1:-1]
            exDivDate = re.findall('>.*?<',str(rows[i].find_all('td')[1]))[-1][1:-1]
            date = datetime.strptime(exDivDate, "%m/%d/%Y")
            euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year) 
            div = re.findall('>.*?<',str(rows[i].find_all('td')[2]))[-1][1:-1]
            annualDiv = re.findall('>.*?<',str(rows[i].find_all('td')[3]))[-1][1:-1]
            recordDate = re.findall('>.*?<',str(rows[i].find_all('td')[4]))[-1][1:-1]
            announceDate = re.findall('>.*?<',str(rows[i].find_all('td')[5]))[-1][1:-1]
            paymentDate = re.findall('>.*?<',str(rows[i].find_all('td')[6]))[-1][1:-1]
        
            cols = [company,
            symbol,
            'Dividend',
            exDivDate,
            euroDate,
            div,
            annualDiv,
            recordDate,
            announceDate,
            paymentDate
            ]
            data.append(cols)
    except AttributeError:
        print("No available data for " + date.strftime('%m-%d-%Y')) 

    #set date 
    date = date + timedelta(days=1)

#write data to csv
with open ('D:\\Safe_IKF\\IKF_DimaN\\Projects\\Web_data_scrapers\\Output_files\\NADSAQ-div-'+start.strftime('%m-%d-%Y')+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)
