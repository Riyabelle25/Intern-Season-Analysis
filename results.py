import requests
from bs4 import BeautifulSoup as soup
from lxml import html
import json
import pprint

# Mohit's creds:-
USERNAME = "add creds here"
PASSWORD = "add creds"

# Parent URLs:-
LOGIN_URL = "http://people.iitr.ernet.in/login/?next=/internship/company/list/#all_companies"
urls = ["http://people.iitr.ernet.in/internship/results/2019/branch/","http://people.iitr.ernet.in/internship/results/2019/company/","http://people.iitr.ernet.in/internship/results/2020/branch/" , "http://people.iitr.ernet.in/internship/results/2020/company/"]

def main():
	session_requests = requests.session()

# Get login csrf token
	result = session_requests.get(LOGIN_URL)
	tree = html.fromstring(result.text)
	authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
	print(authenticity_token)

# Create payload
	payload = {
		"username": USERNAME,
		"password": PASSWORD,
		"csrfmiddlewaretoken": authenticity_token
	}

# Perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
	print("login successful")

# initialising parent dicts:
	branchwiseResults2020 = {}
	branchwiseResults2019 = {}
	companywiseResults2020 = {}
	companywiseResults2019 = {}

# initialising lists:
	page_soup = []

	branchResults = []
	branchResults2019 = []
	companyResults = []
	companyResults2019 = []
	
	tmpCodes = []
	tmpCodes2019 = []
	tmpIDs = []
	tmpIDs2019 = []
	

# Storing html content from nested urls:

	for URL in urls:
		result = session_requests.get(URL, headers = dict(referer = URL))
		page_soup = (soup(result.text,"html.parser"))

		for row in page_soup.find_all('tr'):
			for data in row.find_all('td'):
				
				for url in data.find_all('a' , href = True):
					

			# Fetching 2019 results first:	
					if ('2019' in url['href']):
						
						if('company' not in url['href']):
							x = list(url['href'].split('/'))
							tmpCodes2019.append(x[-2])
							result = session_requests.get("http://people.iitr.ernet.in" + url['href'])
							branchResults2019.append(soup(result.text,"html.parser"))
						

						if('branch' not in url['href']):
							tmpIDs2019.append(list(url['href'].split('/'))[-2])
							result = session_requests.get("http://people.iitr.ernet.in" + url['href'])
							companyResults2019.append(soup(result.text,"html.parser"))
			# Then getting 2020 results:
					else:
			
						if('company' not in url['href']):
							tmpCodes.append(list(url['href'].split('/'))[-2])
							result = session_requests.get("http://people.iitr.ernet.in" + url['href'])
							branchResults.append(soup(result.text,"html.parser"))

						if('branch' not in url['href']):
							tmpIDs.append(list(url['href'].split('/'))[-2])
							result = session_requests.get("http://people.iitr.ernet.in" + url['href'])
							companyResults.append(soup(result.text,"html.parser"))

# First fetching current Branchwise results:
	# print(tmpIDs2019)
	# print(tmpCodes2019)
	# print(tmpIDs)
	# print(tmpCodes)

	for x,branch in enumerate(branchResults):
		BigDictkaList = []
		for row in branch.find_all('tr'):
			tmp = {}
			tmp1 = [] 

			for data in row.find_all('td'):
				tmp1.append(data.contents[0])

			for i in tmp1[1::6]:
				tmp['Enrollment no:'] = i
			for i in tmp1[2::6]:
				tmp['Name:'] = i
			for i in tmp1[3::6]:	
				tmp['Company:'] = i
			for i in tmp1[4::6]:
				tmp['Course:'] = i
			for i in tmp1[5::6]:
				tmp['Accepted:'] = i

				BigDictkaList.append(tmp)
		branchwiseResults2020[tmpCodes[x]] = BigDictkaList

	#pprint.pprint(branchwiseResults2020)

# Repeating iterations for fetchin current results Companywise

	for x,company in enumerate(companyResults):
		BigDictkaList = []
		for row in company.find_all('tr'):
			tmp = {}
			tmp1 = [] 

			for data in row.find_all('td'):
				tmp1.append(data.contents[0])

			for i in tmp1[1::6]:
				tmp['Enrollment no:'] = i
			for i in tmp1[2::6]:
				tmp['Name:'] = i
			for i in tmp1[3::6]:	
				tmp['Branch:'] = i
			for i in tmp1[4::6]:
				tmp['Course:'] = i
			for i in tmp1[5::6]:
				tmp['Accepted:'] = i

				BigDictkaList.append(tmp)
		companywiseResults2020[tmpIDs[x]] = BigDictkaList

	#pprint.pprint(companywiseResults2020)

# Getting 2019 results branchwise:

	for x,branch in enumerate(branchResults2019):
		BigDictkaList = []
		for row in branch.find_all('tr'):
			tmp = {}
			tmp1 = [] 

			for data in row.find_all('td'):
				tmp1.append(data.contents[0])

			for i in tmp1[1::6]:
				tmp['Enrollment no:'] = i
			for i in tmp1[2::6]:
				tmp['Name:'] = i
			for i in tmp1[3::6]:	
				tmp['Company:'] = i
			for i in tmp1[4::6]:
				tmp['Course:'] = i
			for i in tmp1[5::6]:
				tmp['Accepted:'] = i

				BigDictkaList.append(tmp)
		branchwiseResults2019[tmpCodes2019[x]] = BigDictkaList

	#pprint.pprint(branchwiseResults2019)



# Getting 2019 results companywise:

	for x,company in enumerate(companyResults2019):
		BigDictkaList = []
		for row in company.find_all('tr'):
			tmp = {}
			tmp1 = [] 

			for data in row.find_all('td'):
				tmp1.append(data.contents[0])

			for i in tmp1[1::6]:
				tmp['Enrollment no:'] = i
			for i in tmp1[2::6]:
				tmp['Name:'] = i
			for i in tmp1[3::6]:	
				tmp['Branch:'] = i
			for i in tmp1[4::6]:
				tmp['Course:'] = i
			for i in tmp1[5::6]:
				tmp['Accepted:'] = i

				BigDictkaList.append(tmp)
		companywiseResults2019[tmpIDs2019[x]] = BigDictkaList

	#pprint.pprint(companywiseResults2019)


# Dumping dicts prettily into respective json files:
	with open("BranchwiseResults2020.json","w") as outfile:
		json.dump(branchwiseResults2020 , outfile)
	with open("BranchwiseResults2019.json","w") as outfile:
		json.dump(branchwiseResults2019 , outfile)
	with open("CompanywiseResults2019.json","w") as outfile:
		json.dump(companywiseResults2019 , outfile)
	with open("CompanywiseResults2020.json","w") as outfile:
		json.dump(companywiseResults2020 , outfile)

if __name__ == '__main__':
	main()

