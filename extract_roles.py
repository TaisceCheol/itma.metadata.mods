# -*- coding: utf-8 -*-
# import csv,re,difflib,timeit
import csv,re,click
from lxml import etree
from glob import glob 
from fuzzywuzzy import process as fuzzyproc

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

def main_parse(record,REFNO,TYPE):
	global roles,locations,people
	record = record.replace('=','')
	tokenize = record.split(',')
	tokenize = [x.strip() for x in tokenize]
	data = {'name':[],'role':[],'locations':[],'TYPE':TYPE,'REFNO':REFNO}
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

def join_same_name(data):
	store = {}
	for item in data:
		if item['name'] in store.keys():
			store[item['name']]['role'] += item['role']
			store[item['name']]['role'] = list(set(store[item['name']]['role']))
			store[item['name']]['locations'] += item['locations']
			store[item['name']]['locations'] = list(set(store[item['name']]['locations']))
		else:
			store[item['name']] = item
	return store.values()

def format_as_xml(obj):
	el = etree.Element(obj['TYPE'].title())
	el.attrib['id'] = obj['REFNO']
	name = etree.SubElement(el,'Name')
	name.text = obj['name']
	for role in obj['role']:
		role_el = etree.SubElement(el,'Role')
		role_el.text = role 
	return el


src = "itma.cat.soutron_20160216.xml"

print 'Parsing XML data...'

records = etree.parse(src)

refnos = []
roles = []
people = []
cfields = []
locations = []


[cfields.append(p) for p in records.xpath('/recordlist/record/*[self::Creator or self::Contributors]')]
# [people.append(p) for p in r.xpath('/recordlist/record/People/text()')]
[locations.append(p) for p in records.xpath('/recordlist/record/GeographicalLocation/text()')]

for c in cfields:parse_roles(c.text)

roles = sorted(list(set(roles)))
locations = list(set(locations))

count = 0

role_list = etree.Element("NamedRoles")

recordlist = records.xpath('/recordlist/record')

with click.progressbar(recordlist,label="Extracting roles...",length=20) as bar:
	for r in bar:
		extracted_entities = []
		refno = r.xpath('ITMAReference/text()')
		print refno
		if len(refno) == 0:
			refno = r.attrib['CID']
		else:
			refno = refno[0]
		creators = set(r.xpath('Creator/text()'))
		contributors = set(r.xpath('Contributors/text()'))
		creators = [main_parse(x,refno,'CREATOR') for x in creators]
		contributors = [main_parse(x,refno,'CONTRIBUTOR') for x in contributors]
		for x in creators + contributors:
			if len(x['role']):
				extracted_entities.append(x)
				count += 1
		extracted_entities = join_same_name(extracted_entities)
		xml_records = [format_as_xml(x) for x in extracted_entities]
		for el in xml_records:
			# print el
			role_list.append(el)

etree.ElementTree(role_list).write("itma.roles.xml",pretty_print=True)

# with open('itma.roles.csv','w') as f:
# 	writer = csv.writer(f,delimiter=',')
# 	writer.writerow(["REFNO","TYPE","NAME","ROLE","LOCATION"])
# 	for p in extracted_entities:
# 		row = [p['REFNO'].encode('UTF-8'),p['TYPE'],p['name'].encode('UTF-8'),[x.encode('UTF-8') for x in p['role']],[x.encode('UTF-8') for x in p['locations']]]
# 		print [row]
# 		writer.writerow(row)







