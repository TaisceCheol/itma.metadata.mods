import json,click
from multiprocessing.dummy import Pool
from fuzzywuzzy import process
from lxml import etree
from itertools import repeat

def make_instance(el):
	obj = {}
	obj['authorityURI'] = el.attrib['authorityURI']
	obj['valueURI'] = el.attrib['valueURI']
	obj['refno'] = el.attrib['id']
	if len(el.xpath('Language/text()')):
		obj['lang'] = el.xpath('Language/text()')[0]
	return obj

def process_role(role,el):
	global missed_terms,linked_roles
	term = role.text
	print role
	if not term in linked_roles['term_lookup'].keys():
		nearest_term = process.extractOne(term,linked_roles['term_lookup'].keys())
		if nearest_term[-1] > 90:
			term = nearest_term[0]
		else:
			missed_terms.append(term)
			term = None
	if term != None:
		canonical_term = linked_roles['term_lookup'][term]
		data = linked_roles[canonical_term]
		role.attrib['authorityURI'] = data['source']['value']
		role.attrib['valueURI'] = data['entity']['value']
		role.attrib['code'] = data['entity']['value'].split('/')[-1]
		lang = el.xpath('Language')
		if len(lang):
			for lang_el in lang:
				if lang_el.text:
					role.attrib['lang'] = lang_el.text

def process_role_list(el):
	global linked_role_data
	roles = el.xpath('Role')
	map(process_role,roles,repeat(el,len(roles)))
	linked_role_data.append(el)

roles = etree.parse('../itma.roles.xml')
linked_role_data = etree.Element("NamedRoles")

with open('../linked_roles_lookup.json','r') as f:
	linked_roles = json.load(f)

missed_terms = []

role_list = roles.xpath('//NamedRole')[0:10]
pool = Pool(processes=4)

map(process_role_list,role_list)

etree.ElementTree(linked_role_data).write('../itma.roles.linked.xml',pretty_print=True)

with open('../unresolved_terms.txt','w') as f:
	for item in set(sorted(missed_terms)):
		f.write("%s\n" % item.encode('utf-8'))
