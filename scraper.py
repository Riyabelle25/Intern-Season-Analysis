# For GS:-
# LOGIN_URL = "http://people.iitr.ernet.in/login/?next=/internship/company/<id>/info/"
# URL = "http://people.iitr.ernet.in/internship/company/<id>/info/"

#Accepting kis kis ko:-
# LOGIN_URL = "http://people.iitr.ernet.in/login/?next=/internship/company/<id>/opento/"
# URL= "http://people.iitr.ernet.in/internship/company/<id>/opento/"

import requests
from bs4 import BeautifulSoup as soup
from lxml import html
import json

# Mohit's creds:-
USERNAME =  "add creds here"
PASSWORD = "add creds here"

# URLs:-
LOGIN_URL = "http://people.iitr.ernet.in/login/?next=/internship/company/list/#all_companies"
urls = [ "http://people.iitr.ernet.in/internship/company/list/#all_companies", 
"http://people.iitr.ernet.in/internship/results/2013/branch/",
"http://people.iitr.ernet.in/internship/results/2014/branch/",
"http://people.iitr.ernet.in/internship/results/2015/branch/",
"http://people.iitr.ernet.in/internship/results/2016/branch/",
"http://people.iitr.ernet.in/internship/results/2017/branch/",
"http://people.iitr.ernet.in/internship/results/2018/branch/",
"http://people.iitr.ernet.in/internship/results/2019/branch/",
"http://people.iitr.ernet.in/internship/results/2020/branch/"]

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

	# Scrape for ids and branches from 2 different urls: 
	page_soup = []
	for URL in urls:
		result = session_requests.get(URL, headers = dict(referer = URL))
		page_soup.append(soup(result.text,"html.parser"))

	# Map ids to their company names in a dict:
	ID={}
	for row in page_soup[0].find_all('tr'):
		for data in row.find_all('td'):
			for company in data.find_all('a', id= False):
				if (company.contents[0] != 'View'):
					Company = (company.contents)
				
			for Id in data.find_all('a', id= True):
				IDs = (Id['id'][10:])
				ID[IDs] = Company[0]

	# Dump dict IDs to Json file: 
	with open("IDs.json","w") as outfile:
		json.dump(ID , outfile)

	# Now map branches to their codes in a dict:
	Branches = {}
	for page in page_soup:
		for row in page.find_all('tr'):
			for data in row.find_all('td'):
				if " | " in data.contents[0]:
					branch, branch_code = (data.contents[0]).split(' | ')
					Branches[branch] = branch_code
	
	# Dump dict Branches Json file :
	with open("Branches.json","w") as outfile2:
		json.dump(Branches , outfile2)	


if __name__ == '__main__':
	main()

