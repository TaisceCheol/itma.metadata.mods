# -*- coding: utf-8 -*-
import csv,re,difflib,timeit
from lxml import etree
from glob import glob 
from fuzzywuzzy import process as fuzzyproc

def clean_string(text):
	replace = re.compile(ur"(?:\?|\=|(\[\]))")
	clean = replace.sub('',text)
	replace = re.compile(ur"(?:(\s\(\s)|(\s\)\s)|(\]\s\[)|(\)\s\())")
	clean = replace.sub(' ',text)
	replace = re.compile(ur"(\bon\b\s(?:A|B))$")
	clean = replace.sub('',clean).strip()
	replace = re.compile(ur"^((?:A|B)\/\d)")
	clean = replace.sub('',clean).strip()
	replace = re.compile(ur'^(\d+\s*)')
	return replace.sub('',clean).strip()


records = [etree.parse(x) for x in glob('record_groups/**/**.xml')]

people = []

for r in records:
	[people.append(p) for p in r.xpath('/recordlist/record/People/text()')]

# remove zero length
people = filter(lambda x:len(x) > 1,map(clean_string,list(set(people))))
# sorted by first name
people = sorted(people,key=lambda x:x.split()[0])
# sorted by second name
people = sorted(people,key=lambda x:x.split()[-1])

with open('itma.people.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	writer.writerow(["ID","NAME"])
	for i,p in enumerate(people):
		# print [p]
		writer.writerow([i,p.encode('UTF-8')])
