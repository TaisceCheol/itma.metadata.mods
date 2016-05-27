import csv,re,difflib
from lxml import etree
from glob import glob 

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
		if item in locations:
			data['locations'].append(item)
			remove.append(item)
	for item in remove:
		record = record.replace(item,'').replace(',','')
	name_record = record.split()
	name_record.reverse()
	name_record = " ".join(name_record)
	data['name'] = difflib.get_close_matches(name_record,people,1)
	if len(data['name']) == 0:
		data['name'] = record.strip()
	return data

records = [etree.parse(x) for x in glob('record_groups/**/**.xml')[10:11]]

refnos = []
roles = []
people = []
cfields = []
locations = []

for r in records:
	[cfields.append(p) for p in r.xpath('/recordlist/record/*[self::Creator or self::Contributors]')]
	[people.append(p) for p in r.xpath('/recordlist/record/People/text()')]
	[locations.append(p) for p in r.xpath('/recordlist/record/GeographicalLocation/text()')]

for c in cfields:parse_roles(c.text)
roles = sorted(list(set(roles)))
people = filter(remove_with_funny_characters,sorted(list(set(people)),key=lambda x:x.split()[-1]))
locations = list(set(locations))

extracted_entities = []

for group in records:
	for r in group.xpath('/recordlist/record'):
		# print etree.tostring(r,pretty_print=True)
		refno = r.xpath('ITMAReference/text()')[0]
		creators = r.xpath('Creator/text()')
		contributors = r.xpath('Contributors/text()')
		creators = [main_parse(x) for x in creators]
		contributors = [main_parse(x) for x in contributors]
		for x in creators:
			x['REFNO'] = refno 
			x['TYPE'] = 'CREATOR'
			extracted_entities.append(x)			
		for x in contributors:
			x['REFNO'] = refno
			x['TYPE'] = 'CONTRIBUTOR'
			extracted_entities.append(x)
		if len(extracted_entities) > 500:
			break

with open('itma.roles.test.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	writer.writerow(["REFNO","TYPE","NAME","ROLE","LOCATION"])
	for p in extracted_entities:
		writer.writerow([p['REFNO'],p['TYPE'],"".join(p['name']).encode('UTF-8')," | ".join(p['role']).encode('UTF-8'),p['locations']])
