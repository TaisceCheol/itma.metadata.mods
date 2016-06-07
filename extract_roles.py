# -*- coding: utf-8 -*-
import csv,re,difflib,timeit
from lxml import etree
from glob import glob 
from fuzzywuzzy import process as fuzzyproc

start = timeit.timeit()

def remove_with_funny_characters(x):
	if len(x) > 1 and len(x.split()) > 1 and x.find('=') == -1 and x.find('?') == -1:
		return x 

def parse_roles(record):
	global roles
	for x in record.split(','):
		if len(x.split()) and x.split()[0].strip().islower():
			if len(x.split()) <= 3 and x.split()[0] != 'and':
				roles.append(prepare_roles(x))

def prepare_roles(value):
	newvalue = value.strip()
	newvalue = re.sub("[A-Za-z]\d","",newvalue)
	newvalue = re.split("(.*)\son\s.*",newvalue)[0]
	newvalue = re.sub("(?:\d|\=|\?|\[|\]|\)|\(|A|B|\/)","",newvalue)
	return newvalue.strip()

def main_parse(record):
	global roles,locations,people
	record = record.replace('=','')
	tokenize = record.split(',')
	tokenize = [x.strip() for x in tokenize]
	data = {'name':[],'role':[],'locations':[]}
	remove = []
	for item in tokenize:
		if item in roles:
			data['role'].append(item)
			remove.append(item)
		# composer is a role... keep track info with role
		elif item.find('composer') != -1:
			data['role'].append(item)
			remove.append(item)
		if item in locations:
			data['locations'].append(item)
			remove.append(item)
	for item in remove:
		record = record.replace(item,'').replace(',','')
	name_record = record.split()
	name_record.reverse()
	name_record = " ".join(name_record)
	data['name'] = name_record
	# data['name'] = difflib.get_close_matches(name_record,people,1)
	# fuzzy_match = fuzzyproc.extractOne(name_record,people)
	# if fuzzy_match[-1] > 90:
	# 	data['name'] = fuzzy_match[0]
	if len(data['name']) == 0:
		data['name'] = record.strip()
	return data


records = [etree.parse(x) for x in glob('record_groups/**/**.xml')]

refnos = []
roles = []
people = []
cfields = []
locations = []

for r in records:
	[cfields.append(p) for p in r.xpath('/recordlist/record/*[self::Creator or self::Contributors]')]
	# [people.append(p) for p in r.xpath('/recordlist/record/People/text()')]
	[locations.append(p) for p in r.xpath('/recordlist/record/GeographicalLocation/text()')]

for c in cfields:parse_roles(c.text)

roles = sorted(list(set(roles)))
locations = list(set(locations))

# people = filter(remove_with_funny_characters,sorted(list(set(people)),key=lambda x:x.split()[-1]))

# with open('itma.people.csv','w') as f:
# 	writer = csv.writer(f,delimiter=',')
# 	writer.writerow(["ID","NAME"])
# 	for i,p in enumerate(people):
# 		writer.writerow([i,p.encode('UTF-8')])


extracted_entities = []

count = 0

for group in records:
	for i,r in enumerate(group.xpath('/recordlist/record')):
		# print etree.tostring(r,pretty_print=True)
		refno = r.xpath('ITMAReference/text()')
		if len(refno) == 0:
			refno = r.attrib['CID']
		else:
			refno = refno[0]
		print 'Processing: %s' % refno
		creators = r.xpath('Creator/text()')
		contributors = r.xpath('Contributors/text()')
		creators = [main_parse(x) for x in creators]
		contributors = [main_parse(x) for x in contributors]
		for x in creators:
			x['REFNO'] = refno 
			x['TYPE'] = 'CREATOR'
			extracted_entities.append(x)			
			count += 1

		for x in contributors:
			x['REFNO'] = refno
			x['TYPE'] = 'CONTRIBUTOR'
			extracted_entities.append(x)
			count += 1

with open('itma.roles.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	writer.writerow(["REFNO","TYPE","NAME","ROLE","LOCATION"])
	for p in extracted_entities:
		row = [p['REFNO'].encode('UTF-8'),p['TYPE'],p['name'].encode('UTF-8'),[x.encode('UTF-8') for x in p['role']],[x.encode('UTF-8') for x in p['locations']]]
		print [row]
		writer.writerow(row)







