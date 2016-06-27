import json,click
from multiprocessing.dummy import Pool
from fuzzywuzzy import process
from lxml import etree
from itertools import repeat

class MapR():

	def __init__(self,roles_file,roles_lookup,linked_roles,unresolved_terms_path='unresolved_terms.txt'):	
		roles = etree.parse(roles_file)
		self.linked_role_data = etree.Element("NamedRoles")

		with open(roles_lookup,'r') as f:
			self.linked_roles = json.load(f)

		self.missed_terms = []

		role_list = roles.xpath('//NamedRole')
		pool = Pool(processes=4)

		map(self.process_role_list,role_list)

		etree.ElementTree(self.linked_role_data).write(linked_roles,pretty_print=True)

		with open(unresolved_terms_path,'w') as f:
			for item in set(sorted(self.missed_terms)):
				f.write("%s\n" % item.encode('utf-8'))

	def make_instance(self,el):
		obj = {}
		obj['authorityURI'] = el.attrib['authorityURI']
		obj['valueURI'] = el.attrib['valueURI']
		obj['refno'] = el.attrib['id']
		if len(el.xpath('Language/text()')):
			obj['lang'] = el.xpath('Language/text()')[0]
		return obj

	def process_role(self,role,el):
		term = role.text
		if not term in self.linked_roles['term_lookup'].keys():
			nearest_term = process.extractOne(term,self.linked_roles['term_lookup'].keys())
			if nearest_term[-1] > 90:
				term = nearest_term[0]
			else:
				self.missed_terms.append(term)
				term = None
		if term != None:
			canonical_term = self.linked_roles['term_lookup'][term]
			data = self.linked_roles[canonical_term]
			role.attrib['authorityURI'] = data['source']['value']
			role.attrib['valueURI'] = data['entity']['value']
			role.attrib['code'] = data['entity']['value'].split('/')[-1]
			lang = el.xpath('Language')
			if len(lang):
				for lang_el in lang:
					if lang_el.text:
						role.attrib['lang'] = lang_el.text

	def process_role_list(self,el):
		roles = el.xpath('Role')
		map(self.process_role,roles,repeat(el,len(roles)))
		self.linked_role_data.append(el)

