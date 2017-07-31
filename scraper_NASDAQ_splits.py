
#Author: David Nie 
#call with "python <prgm name> <date in format m/d/Y> <date in format m/d/Y>

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import sys
from datetime import datetime, timedelta, date

data = [["Company Name", "Symbol", "Event_type", "Ratio", "Payable", "Ex-Date", "Ex-Date (Euro)", "Announced"]]

nasdaq = "http://www.nasdaq.com/markets/upcoming-splits.aspx"

page = urllib.request.urlopen(nasdaq)
soup = bs.BeautifulSoup(page,'html.parser')
table = soup.find('table',{'id':'two_column_main_content_Upcoming_Splits'})
rows = table.find_all('tr')[1:]



for i in range(len(rows)):
	company = re.findall('.*?[(]',rows[i].a.string)[0][:-2]  # use more beautiful soup for future refs
	company = re.sub(r'&amp;', r'&', company)
	company = re.sub(r';', r'', company)

	symbol = re.findall('[(][A-Za-z ]*?[)]',str(rows[i]))[-1][1:-1]
	d = rows[i].find_all('td')
	ratio = str(d[1])[4:-5]
	payable = str(d[2])[4:-5]
	exDate = str(d[3])[4:-5]
	date = datetime.strptime(exDate, "%m/%d/%Y")
	euroDate = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
	announce = str(d[4])[4:-5]

	cols=[company, symbol,"Splits",ratio,payable,exDate,euroDate,announce]
	data.append(cols)

today = datetime.combine(date.today(), datetime.min.time())
with open ('NADSAQ-splits-'+str.split(str(today))[0]+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)
