import re
from lxml import etree

src = "ITMA-catalogue_20160216.xml"

element_list = etree.Element("recordlist")

with open(src,'r') as f:
	data = "".join(f.readlines()).replace('\r\n','')
	splitter = re.findall(u'<row cid="\d+" Deleted="0">((?:(?!<\/row>).)*)',data,re.DOTALL)
	for i,el in enumerate(splitter):
		node = etree.fromstring("<record>%s</record>" % el)
		node.set('CID', unicode(i+1))
		element_list.append(node)

etree.ElementTree(element_list).write("itma.cat.soutron_20160216.xml",pretty_print=True,encoding='UTF-8')