import json,click
from lxml import etree
from itertools import repeat
from multiprocessing.dummy import Pool
import time

start_time = time.time()

def process_match(item,name):
	roles = item.xpath('Role')
	for role in roles:
		name.append(role)

def process_name(name,refno):
	global pool
	print name,refno
	match = linked_roles.xpath('/NamedRoles/NamedRole[@id="%s"][Name/text()="%s"]' % (refno,name.text))
	if len(match):
		name.attrib['name'] = name.text	
		name.text = None
		map(process_match,match,repeat(name,len(match)))

def process_record(record):
	global linked_cat
	refno = record.attrib['CID']
	people = record.xpath('People')
	if len(people):
		map(process_name,people,repeat(refno,len(people)))
	linked_cat.append(record)
	return None

# import source records
print 'Reading catalogue records'
catalogue = etree.parse('itma.cat.soutron_20160216.xml')
linked_roles = etree.parse('itma.roles.linked.xml')
print 'Catalogue records read'
# root node for linked records
linked_cat = etree.Element('recordlist')

# multiprocessing pool
pool = Pool(processes=4)
# list of source records
records = catalogue.xpath('/recordlist/record')
# process records
pool.map(process_record,records)

# write linked catalogue xml
etree.ElementTree(linked_cat).write('itma.linked.cat.xml',pretty_print=True)

print "--- %s ---" % (time.time() - start_time)
