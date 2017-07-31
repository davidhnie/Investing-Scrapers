#Author: David 

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import sys
from datetime import datetime, timedelta, date

link="http://www.nasdaq.com/earnings/daily-earnings-surprise.aspx?reportdate="

data=[["Company","Symbol","Market","Event_type","Date","Quarter","EPS","Forecast","# Estimates","% Surprise", "Footer Date"]]
types=["Exceeded","Met","Failed"]
s1= sys.argv[1]
s2= sys.argv[2]
date = datetime.strptime(s1, "%m/%d/%Y")
end = datetime.strptime(s2, "%m/%d/%Y")
start = date

while date<=end:


	page = urllib.request.urlopen(link+str(date.year)+str(date.month).zfill(2)+str(date.day).zfill(2))
	soup = bs.BeautifulSoup(page,'html.parser')

	table = soup.find_all('div',{'class':'genTable'})

	
	for j in range(3):
		rows=table[j].find_all('tr')[1:]
		for i in range(len(rows)):
			
			company=rows[i].find_all('a')[0].string
			company = re.sub(r'&amp;', r'&', company)
			company = re.sub(r';', r'', company)

			symbol=rows[i].find_all('a')[1].string
			market=rows[i].div.contents[-1].strip()

			tds=rows[i].find_all('td')[1:]

			quarter=tds[0].contents[0]
			quarter = str(quarter).replace(u'\xa0', u' ')

			EPS=tds[1].contents[0]
			forecast=tds[2].contents[0]
			ests=tds[3].contents[0]
			surprise=tds[4].contents[0]

			footer=soup.find('div',{'class':'floatR marginT10px TalignR'})
			footer=footer.small.contents[-1].strip()[12:]

			cols=[company, symbol, market, types[j], date.strftime('%m-%d-%Y'), quarter, EPS, forecast, ests, surprise, footer]
			data.append(cols)
	#set date 
	date = date + timedelta(days=1)

	#european date

#write data to csv
with open ('NADSAQ-surprise-'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)
