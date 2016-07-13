import json,click,re
from lxml import etree
from itertools import repeat
from multiprocessing.dummy import Pool
import time
from xml.sax.saxutils import escape

class Link():
	
	def __init__(self,records,linked_roles_path,linked_catalog_path,linked_places):
		# import source records
		print 'Reading catalogue records'
		#catalogue = etree.parse(catalog_path)
		self.linked_roles = etree.parse(linked_roles_path)
		#records = catalogue.xpath('/recordlist/record')
		self.linked_cat = etree.Element('recordlist')				
		self.locations = etree.parse(linked_places)

		pool = Pool(processes=4)
		map(self.process_record,records)
		# write linked catalogue xml
		etree.ElementTree(self.linked_cat).write(linked_catalog_path,pretty_print=True)
		print '::-- Process Complete --::'
		
	def process_match(self,item,name):
		roles = item.xpath('Role')
		for role in roles:
			name.append(role)

	def process_name(self,name,cid):
		query_string = '/NamedRoles/NamedRole[@id="%s"][Name/text()="%s"]' % (cid,name.text.replace('"','&quot;'))
		match = self.linked_roles.xpath(query_string)
		if len(match):
			name.attrib['name'] = name.text	
			name.text = None
			map(self.process_match,match,repeat(name,len(match)))
			if 'viaf_url' in match[0].attrib.keys():
				name.attrib['viaf-url'] = match[0].attrib['viaf_url']

	def process_record(self,record):
		cid = record.attrib['CID']
		people = record.xpath('People')
		if len(people):
			map(self.process_name,people,repeat(cid,len(people)))
		self.link_places(record,cid)
		self.linked_cat.append(record)

	def link_places(self,record,cid):
		match = self.locations.xpath('/Locations/Location[@catid="%s"]' % cid)
		for item in match:
			record.append(item)



