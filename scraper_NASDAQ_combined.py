#Author: David Nie

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import sys
from datetime import datetime, timedelta, date

#call with command line 
s1= sys.argv[1]#"07/07/2017"#sys.argv[1]
s2= sys.argv[2]#"07/17/2017"#sys.argv[2]
date = datetime.strptime(s1, "%m/%d/%Y")
end = datetime.strptime(s2, "%m/%d/%Y")
start = date

#DIVIDENDS
nasdaq = "http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date="

data = [["Ticker","European_date", "Event_type"]] #ticker, date, event_type
while date<=end :
	page = urllib.request.urlopen(nasdaq+str(date.year)+'-'+str(date.month)+'-'+str(date.day))

	soup = bs.BeautifulSoup(page,'html.parser')

	#correctly id the table
	table = soup.find('table',{'id':'Table1'})

	# HANDLE NON-AVAILABE TRADE DAYS . . . . . 
	try:
		table_body=table.find('tbody')
		rows = table_body.find_all('tr')
		for i in range(len(rows)):
			symbol = re.findall('[(].*?[)]', str(rows[i].td.a))[-1][1:-1]
			exDivDate = re.findall('>.*?<',str(rows[i].find_all('td')[1]))[-1][1:-1]
			date = datetime.strptime(exDivDate, "%m/%d/%Y")
			euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year) 
			cols = [symbol,euroDate,"Dividends"]
			data.append(cols)

	except AttributeError:
		print("No available data for dividends on " + date.strftime('%m-%d-%Y'))

	date = date + timedelta(days=1)

#EARNINGS
date = start
nasdaq = "http://www.nasdaq.com/earnings/earnings-calendar.aspx?date="

while date<=end :

	page = urllib.request.urlopen(nasdaq+str(date.year)+'-'+str(date.month)+'-'+str(date.day))
	soup = bs.BeautifulSoup(page,'html.parser')

        #correctly id tables
	tables = soup.find_all('table',{'class':'USMN_EarningsCalendar'})

	try:
                #CONFIRMED DATA
		rows=tables[0].find_all('tr')[1:]
        
		for i in range(len(rows)):
			rows=tables[0].find_all('tr')[1:]
			symbol = re.findall('[(].*?[)]', str(rows[i]))[-1][1:-1]
			reportDate = re.findall('../../....',str(rows[i].find_all('td')[2]))[0]
			date = datetime.strptime(reportDate, "%m/%d/%Y")
			euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year) 
			try:
				time = re.findall('title=".*?">',str(rows[i].find_all('td')[0]))[0][7:-3] 
			except IndexError:
				time = "n/a"
				
			cols = [symbol,euroDate,"Earnings-confirmed-"+time]
			data.append(cols)
	except IndexError:
		print("No available data for confirmed on " + date.strftime('%m-%d-%Y'))
	try:
                #ESTIMATED DATA
		rows=tables[1].find_all('tr')[1:]
    

		for i in range(len(rows)):
			symbol = re.findall('[(].*?[)]', str(rows[i]))[-1][1:-1] 
			reportDate = re.findall('../../....',str(rows[i].find_all('td')[1]))[0]
			date = datetime.strptime(reportDate, "%m/%d/%Y")
			euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year)

			cols = [symbol, euroDate, "Earnings-estimated-n/a"]
			data.append(cols)
	except IndexError:
		print("No available data for estimated on " + date.strftime('%m-%d-%Y'))
	date = date + timedelta(days=1)

#SPLITS
nasdaq = "http://www.nasdaq.com/markets/upcoming-splits.aspx"

page = urllib.request.urlopen(nasdaq)
soup = bs.BeautifulSoup(page,'html.parser')
table = soup.find('table',{'id':'two_column_main_content_Upcoming_Splits'})
rows = table.find_all('tr')[1:]

for i in range(len(rows)):
	symbol = re.findall('[(][A-Za-z ]*?[)]',str(rows[i]))[-1][1:-1]
	d = rows[i].find_all('td')
	exDate = str(d[3])[4:-5]
	date = datetime.strptime(exDate, "%m/%d/%Y")
	euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year)

	cols = [symbol, euroDate, "Splits"]
	data.append(cols)
with open ('NADSAQ-combined-'+str.split(str(start))[0]+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)


