import json,click
from fuzzywuzzy import process
from lxml import etree

roles = etree.parse('itma.roles.xml')
linked_role_data = etree.Element("NamedRoles")

with open('linked_roles_lookup.json','r') as f:
	linked_roles = json.load(f)

with click.progressbar(roles.xpath('//NamedRole'),label="Linking to authority files...") as bar:
	for el in bar:
		value = el.xpath('Role/text()')
		if len(value):
			for term in value:
				if not term in linked_roles['term_lookup'].keys():
					nearest_term = process.extractOne(term,linked_roles['term_lookup'].keys())
					if nearest_term[-1] > 85:
						term = nearest_term[0]
					else:
						print 'Cannot find term: %s' % term
						break
				canonical_term = linked_roles['term_lookup'][term]
				data = linked_roles[canonical_term]
				el.attrib['authorityURI'] = data['source']['value']
				el.attrib['valueURI'] = data['entity']['value']
			linked_role_data.append(el)
		

etree.ElementTree(linked_role_data).write('itma.roles.linked.xml',pretty_print=True)

