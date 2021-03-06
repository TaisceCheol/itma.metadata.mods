# -*- coding: utf-8 -*-
# import csv,re,difflib,timeit
import csv,click,re
from lxml import etree
from glob import glob 
from fuzzywuzzy import process as fuzzyproc
from multiprocessing.dummy import Pool

class Extract():
	def __init__(self,records,outfile):
		#cat_xml = "../itma.cat.soutron_20160216.xml"
		print 'Parsing XML data...'
		#records = etree.parse(cat_xml)
		self.counter = 0
		self.roles = ['performer']
		self.locations = []
		cfields = []
		refnos = []

		self.records = records
		[[cfields.append(y) for y in x.xpath('*[self::Creator or self::Contributors]')] for x in records]
		[[self.locations.append(y) for y in x.xpath('GeographicalLocation/text()')] for x in records]
		
		map(self.parse_roles,cfields)
		self.roles = list(set([x.replace('\n','').strip() for x in filter(lambda x:len(x) > 1,self.roles)]))
		self.locations = list(set(self.locations))

		self.role_list = etree.Element("NamedRoles")

		self.cache = {}

		print 'extracting roles...'
		pool = Pool(processes=4)
		pool.map(self.process_recordlist,records)
			
		return etree.ElementTree(self.role_list).write(outfile,pretty_print=True)

	def parse_roles(self,record):
		for x in record.text.split(','):
			if len(x.split()) and x.split()[0].strip().islower():
				if len(x.split()) <= 3 and x.split()[0] != 'and' and x.split()[0] != 'various' and x.split()[0] != '[various':
					self.roles.append(self.prepare_roles(x))

	def prepare_roles(self,value):
		newvalue = value.strip()
		newvalue = re.sub("[A-Za-z]\d","",newvalue)
		newvalue = re.split("(.*)\son\s.*",newvalue)[0]
		newvalue = re.sub("(?:\d|\=|\?|\[|\]|\)|\(|A|B|\/|\-)","",newvalue)
		# print 'Role: %s' % newvalue.strip()
		return newvalue.strip()

	def main_parser(self,record,REFNO,TYPE,people,doctype):
		# if "Unidentified" not in people:
			# people.append("Unidentified")
		record = record.replace('=','')
		data = {'name':[],'role':[],'locations':[],'tracks':[],'TYPE':TYPE,'REFNO':REFNO}	
		if record in self.cache.keys():
			# print 'Found cached record: %s' % record
			data['name'] = self.cache[record]['name']
			data['role'] = self.cache[record]['role']
			data['locations'] = self.cache[record]['locations']
			data['tracks'] = self.cache[record]['tracks']
		elif len(people):
			data['name'] = fuzzyproc.extractOne(record,people)[0]
			tracks = re.findall('((?:A|B)\d+(\,*\s*(?:A|B)*\d+)*)',record)
			if len(tracks):
				for y in tracks[0][0].split(','):
					data['tracks'].append(y.strip())
				record = record.replace(tracks[0][0],'\n').strip()
			tokens = filter(lambda x: x not in data['name'].split(),[y.strip() for y in record.split(',')])
			for item in tokens:
				if item in self.roles:
					data['role'].append(item)
				elif item in self.locations:
					data['locations'].append(item)
			self.cache[record] = data
			# print 'Caching record: %s' % record
		else:
			# print 'Caching record: %s' % record
			self.cache[record] = data		
		data['role'] = list(set(data['role']))
		if len(data['role']) == 0 and TYPE == 'CREATOR' and doctype == 'Sound Recording':
			data['role'].append('performer')
		return data

	def join_same_name(self,data):
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

	def format_as_xml(self,obj,dctype):
		el = etree.Element("NamedRole",type=obj['TYPE'].lower())
		el.attrib['id'] = obj['REFNO']
		doctype = etree.SubElement(el,'DocType')
		doctype.text = dctype
		name = etree.SubElement(el,'Name')
		name.text = obj['name']
		if len(obj['role']) >= 2 and 'performer' in obj['role']:
			del obj['role'][obj['role'].index('performer')]		
		for role in obj['role']:
			found_lang_el = False
			# splits singing in Irish/English into singing/voice roles with a language term...
			if role.find('singing') != -1:
			 	role_el = etree.SubElement(el,'Role')
			 	role_el.text = 'singer'
			 	role_el.attrib['lang'] = role.split('in')[-1].strip()
			elif role.find('speech') != -1:
			 	role_el = etree.SubElement(el,'Role')
			 	role_el.text = 'voice'	
			 	role_el.attrib['lang'] = role.split('in')[-1].strip()
			else: 
				role_el = etree.SubElement(el,'Role')
				role_el.text = role
		return el

	def process_recordlist(self,record):
		extracted_entities = []
		refno = record.attrib['CID']
		doctype = record.xpath('DocType/text()')[0]
		people = [x.strip() for x in list(set(record.xpath('People/text()')))]
		creators = set(record.xpath('Creator/text()'))
		contributors = set(record.xpath('Contributors/text()'))
		creators = [self.main_parser(x,refno,'CREATOR',people,doctype) for x in creators]
		contributors = [self.main_parser(x,refno,'CONTRIBUTOR',people,doctype) for x in contributors]
		for x in creators + contributors:
			extracted_entities.append(x)
		extracted_entities = self.join_same_name(extracted_entities)
		extracted_names = [x['name'] for x in extracted_entities]
		if doctype == 'Image':
			depicted = filter(lambda x:x not in extracted_names,people)
			for p in depicted:
				data = {'name':p,'role':['depicted'],'REFNO':refno,'TYPE':'depicted'}	
				extracted_entities.append(data)
		xml_records = [self.format_as_xml(x,doctype) for x in extracted_entities]
		for el in xml_records:
			self.role_list.append(el)
			self.counter += 1
			if self.counter % 1000 == 0:
				print self.counter/float(len(self.records))

