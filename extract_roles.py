# -*- coding: utf-8 -*-
# import csv,re,difflib,timeit
import csv,click,re
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
	newvalue = re.sub("(?:\d|\=|\?|\[|\]|\)|\(|A|B|\/|\-)","",newvalue)
	return newvalue.strip()


def main_parse(record,REFNO,TYPE,people):
	global roles,locations,cache
	if "Unidentified" not in people:
		people.append("Unidentified")
	record = record.replace('=','')
	data = {'name':[],'role':[],'locations':[],'tracks':[],'TYPE':TYPE,'REFNO':REFNO}	

        if record in cache.keys():
		# print 'Found cached record: %s' % record
                data['name'] = cache[record]['name']
                data['role'] = cache[record]['role']
		data['locations'] = cache[record]['locations']
		data['tracks'] = cache[record]['tracks']
	elif len(people):
		data['name'] = fuzzyproc.extractOne(record,people)[0]
		tracks = re.findall('((?:A|B)\d+(\,*\s*(?:A|B)*\d+)*)',record)
		if len(tracks):
			for y in tracks[0][0].split(','):
				data['tracks'].append(y.strip())
			record = record.replace(tracks[0][0],'').strip()
		tokens = filter(lambda x: x not in data['name'].split(),[y.strip() for y in record.split(',')])
		for item in tokens:
			if item in roles:
				data['role'].append(item)
			elif item in locations:
				data['locations'].append(item)
		cache[record] = data
		# print 'Caching record: %s' % record
	else:
		# print 'Caching record: %s' % record
		cache[record] = data		
	return data

def join_same_name(data):
	store = {}
	for item in data:
		if item['name'] in store.keys() and not isinstance(item['name'],list):
			store[item['name']]['role'] += item['role']
			store[item['name']]['role'] = list(set(store[item['name']]['role']))
			store[item['name']]['locations'] += item['locations']
			store[item['name']]['locations'] = list(set(store[item['name']]['locations']))
		elif isinstance(item['name'],list):
			pass
		else:
			store[item['name']] = item
	return store.values()

def format_as_xml(obj):
	el = etree.Element("NamedRole",type=obj['TYPE'].lower())
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
cfields = []
locations = []

[cfields.append(p) for p in records.xpath('/recordlist/record/*[self::Creator or self::Contributors]')]
[locations.append(p) for p in records.xpath('/recordlist/record/GeographicalLocation/text()')]

for c in cfields:parse_roles(c.text)

roles = list(set([x.replace('\n','').strip() for x in filter(lambda x:len(x) > 1,roles)]))
locations = list(set(locations))

role_list = etree.Element("NamedRoles")

recordlist = records.xpath('/recordlist/record')

cache = {}
c = 0
with click.progressbar(recordlist,label="Extracting roles...") as bar:
	for r in bar:
	# for r in recordlist:
		extracted_entities = []
		refno = r.xpath('ITMAReference/text()')
		if len(refno) == 0:
			refno = r.attrib['CID']
		else:
			refno = refno[0]
		people = list(set(r.xpath('People/text()')))
		creators = set(r.xpath('Creator/text()'))
		contributors = set(r.xpath('Contributors/text()'))
		creators = [main_parse(x,refno,'CREATOR',people) for x in creators]
		contributors = [main_parse(x,refno,'CONTRIBUTOR',people) for x in contributors]
		for x in creators + contributors:
			if len(x['role']):
				extracted_entities.append(x)
		extracted_entities = join_same_name(extracted_entities)
		xml_records = [format_as_xml(x) for x in extracted_entities]
		for el in xml_records:
			role_list.append(el)
			c += 1
#		if c > 25: break
	
etree.ElementTree(role_list).write("itma.roles.xml",pretty_print=True)

# with open('itma.roles.csv','w') as f:
# 	writer = csv.writer(f,delimiter=',')
# 	writer.writerow(["REFNO","TYPE","NAME","ROLE","LOCATION"])
# 	for p in extracted_entities:
# 		row = [p['REFNO'].encode('UTF-8'),p['TYPE'],p['name'].encode('UTF-8'),[x.encode('UTF-8') for x in p['role']],[x.encode('UTF-8') for x in p['locations']]]
# 		print [row]
# 		writer.writerow(row)







