#Author: David Nie

#ticker, date, event_type-[upgrades/downgrades/initiated.. . . - from-to] / [exceeded/met/failed-percentage]

import bs4 as bs
import urllib
import urllib.request
import re 
import sys
import csv
from datetime import datetime, timedelta, date

data=[["Ticker", "Date", "Event_type"]]

types1=["Exceeded","Met","Failed"]
types2=["Upgraded","Downgraded","Initiated","Reiterated"]

#surprises
link="http://www.nasdaq.com/earnings/daily-earnings-surprise.aspx?reportdate="

s1= sys.argv[1]
s2= sys.argv[2]
date = datetime.strptime(s1, "%m/%d/%Y")
end = datetime.strptime(s2, "%m/%d/%Y")
start = date
"""
while date<=end:


	page = urllib.request.urlopen(link+str(date.year)+str(date.month).zfill(2)+str(date.day).zfill(2))
	soup = bs.BeautifulSoup(page,'html.parser')

	table = soup.find_all('div',{'class':'genTable'})

	
	for j in range(3):
		rows=table[j].find_all('tr')[1:]
		for i in range(len(rows)):

			symbol=rows[i].find_all('a')[1].string

			tds=rows[i].find_all('td')[1:]
			surprise=tds[4].contents[0]
			footer=soup.find('div',{'class':'floatR marginT10px TalignR'})
			footer=footer.small.contents[-1].strip()[12:]

			cols=[symbol,footer,types1[j]+"-"+surprise]
			data.append(cols)
	#set date 
	date = date + timedelta(days=1)
"""
#updown
link="http://www.nasdaq.com/earnings/daily-analyst-recommendations.aspx?type="


for j in range(4):
	page = urllib.request.urlopen(link+types2[j])
	soup = bs.BeautifulSoup(page,'html.parser')

	table = soup.find('div',{'class':'genTable'})
	rows=table.find_all('tr')[1:]
	for i in range(len(rows)):

		symbol = rows[i].h3.a.string.strip()
		if (j != 2):
			froms = rows[i].find_all('td')[4].string
			tos = rows[i].find_all('td')[5].string
		else:
			froms = rows[i].find_all('td')[4].string
			tos = rows[i].find_all('td')[4].string

		footer=soup.find('div', {'class':'floatR marginT10px'}).small.contents[-1][6:]
		
		if froms is None:
			froms="n/a"
		if tos is None:
			tos="n/a"

		cols = [symbol, footer, types2[j]+"-"+froms+"-"+tos]
		data.append(cols)

with open ('NADSAQ-updown-surprise'+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)



