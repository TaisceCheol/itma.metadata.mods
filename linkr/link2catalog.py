import json,click,re
from lxml import etree
from itertools import repeat
from multiprocessing.dummy import Pool
import time
from xml.sax.saxutils import escape

class Link():
	
	def __init__(self,records,linked_roles_path,linked_catalog_path,linked_places,materials_lookup_path):
		# import source records
		print 'Reading catalogue records'
		#catalogue = etree.parse(catalog_path)
		self.linked_roles = etree.parse(linked_roles_path)
		#records = catalogue.xpath('/recordlist/record')
		self.linked_cat = etree.Element('recordlist')				
		self.locations = etree.parse(linked_places)
		with open(materials_lookup_path,'r') as f:
			self.material_lookup = json.load(f)
		print 'processing records'
		pool = Pool(processes=4)
		map(self.process_record,records)
		# write linked catalogue xml
		print 'writing results'
		etree.ElementTree(self.linked_cat).write(linked_catalog_path,pretty_print=True)
		print '::-- Process Complete --::'
		
	def process_match(self,item,name):
		roles = item.xpath('Role')
		for role in roles:
			name.append(role)

	def process_name(self,name,cid):
		query_string = '/NamedRoles/NamedRole[@id="%s"][Name/text()="%s"]' % (cid,name.text.replace('"','&quot;'))
		match = self.linked_roles.xpath(query_string)
		print name,cid,query_string,match
		if len(match):
			name.attrib['name'] = name.text	
			name.text = None
			map(self.process_match,match,repeat(name,len(match)))
			if 'viaf_url' in match[0].attrib.keys():
				name.attrib['viaf-url'] = match[0].attrib['viaf_url']

	def process_material(self,material):
		term = material.text
		if term in self.material_lookup:
			material_type = self.material_lookup[term]
			material.attrib['getty_uri'] = str(material_type)

	def process_record(self,record):
		cid = record.attrib['CID']
		people = record.xpath('People')
		if len(people):
			map(self.process_name,people,repeat(cid,len(people)))
		material = record.xpath('MaterialType')
		if len(material):
			map(self.process_material,material)
		self.link_places(record,cid)
		self.linked_cat.append(record)

	def link_places(self,record,cid):
		match = self.locations.xpath('/Locations/Location[@catid="%s"]' % cid)
		location_tags = record.xpath('*[self::CreationLocation or self::GeographicalLocation or self::PublisherLocation]')
		for place in location_tags:
			for item in match:
				if place.text == item.text:
					for at in item.attrib:
						place.attrib[at] = item.attrib[at]



