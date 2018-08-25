#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import re
import pprint
import html5lib
from datetime import date


def createHash():

	main_url = "https://www.moneycontrol.com/stocks/marketstats/onlybuyers.php"

	r = requests.get(main_url)

	table_dict = dict()

	soup = BeautifulSoup(r.content,'html5lib')

	for data in soup.findAll('div',{'class':'bsr_table bsr_table930 MT20 PR hist_tbl'}):
		for body in data.findAll('tbody'):
			for tr in body.findAll('tr'):
				for counter,td in enumerate(tr.findAll('td')):
					content = [row for row in td.stripped_strings]
					if len(content) == 12 or len(content) == 11 or len(content) == 10 or len(content) == 7 or len(content) == 8:
						if re.match('^[A-Z\s]+$',content[0].strip()):
							if company == "NDTV":
								company = content[0].strip()
								table_dict[company] = dict()
						elif re.match('^[0-9]+',content[0].strip()):
								pass
						else:
							company = content[0].strip()
							table_dict[company] = dict()

					if counter == 1:
						if len(content) == 1:
							sector = content[0].strip()
							if re.match("^[a-zA-Z]+",sector):
								table_dict[company]['Sector'] = sector
					elif counter == 2:
						table_dict[company]['BidQty'] = content[0].strip()
					elif counter == 3:
						table_dict[company]['LastPrice'] = content[0].strip()
					elif counter == 4:
						table_dict[company]['Diff'] = content[0].strip()
					elif counter == 5:
						table_dict[company]['ChangePer'] = content[0].strip()
	fileDump(table_dict)

def fileDump(hash):
	today = date.today()
	file = open("MoneyControl_tableDump_Intraday_{0}.txt".format(today), "w")

	for outer_key in hash:
		file.write(outer_key+"|")
		for inner_key in hash[outer_key]:
			file.write(hash[outer_key][inner_key]+"|")
		file.write("\n")

	file.close()


if __name__ == "__main__":

    # Creating a nested dictionary and
	#dumping the contents of it in a file

	createHash()
