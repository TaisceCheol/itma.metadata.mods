import json
from lxml import etree

catalogue = etree.parse('itma.cat.soutron_20160216.xml')
linked_roles = etree.parse('itma.roles.linked.xml')

linked_cat = etree.Element('recordlist')

for record in catalogue.xpath('/recordlist/record'):
	refno = record.xpath('ITMAReference/text()')[0]
	people = record.xpath('People')
	for name in people:
		match = linked_roles.xpath('/NamedRoles/NamedRole[@id="%s"][Name/text()="%s"]' % (refno,name.text))
		if len(match):
			name.attrib['name'] = name.text	
			name.text = None
			for item in match:
				roles = item.xpath('Role')
				for role in roles:
					name.append(role)
	linked_cat.append(record)
	break

etree.ElementTree(linked_cat).write('itma.linked.cat.xml',pretty_print=True)
