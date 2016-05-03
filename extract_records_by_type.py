from lxml import etree
import re,subprocess

src = "ITMA-catalogue_20160216.xml"

types = ['Sound Recording','Image','Printed Material','Serial Issue','Video','Copy']

short_names = {'Sound Recording':'sounds','Printed Material':'prints','Serial Issue':'serials','Copy':'copies'}

for doc_type in types:

	for j in ["test","full"]:

		element_list = etree.Element("recordlist")

		with open(src,'r') as f:
			data = "".join(f.readlines()).replace('\r\n','')
			splitter = re.findall(u'<row cid="\d+" Deleted="0">(<DocType>%s</DocType>(?:(?!<\/row>).)*)' % doc_type,data,re.DOTALL)
			for i,el in enumerate(splitter):
				node = etree.fromstring("<record>%s</record>" % el)
				node.set('CID', unicode(i+1))
				element_list.append(node)
				if j == "test" and i > 5000:
					break
			tree = etree.ElementTree(element_list)
			if doc_type in short_names.keys():
				write_name = short_names[doc_type]
			else:
				write_name = doc_type.lower()+'s' 
			if j == "test":
				tree.write("record_groups/itma.recordlist.%s.test.xml"%write_name,encoding='UTF-8',pretty_print=True)
			else:
				tree.write("record_groups/itma.recordlist.%s.xml"%write_name,encoding='UTF-8',pretty_print=True)