from lxml import etree
import re,subprocess

src = "itma.cat.soutron_20160216.xml"

types = ['Sound Recording','Image','Printed Material','Serial Issue','Video','Copy']

short_names = {'Sound Recording':'sounds','Printed Material':'prints','Serial Issue':'serials','Copy':'copies'}

data = etree.parse(src)

carriers = {
	'sounds': {
		'CYL':ur'cyl(inder)',
		'78s':ur'(78\s*(rpm))',
		'LP':ur'(?:LP|L\.P\.)',
		'REEL':ur'(?:reel-to-reel|reel)',
		'CS':ur'(?:CS|cassette)',
		'CD':ur'(?:compact disc|CD|C\.D\.)',
		'WAV':ur'(?:WAVE file|WAV file|wav file)',
		'MP3':ur'(?:MP3|MP3 file)'
	}
}

for carrier in carriers['sounds'].iteritems():
	name = carrier[0]
	regex = carrier[-1]
	element_list = etree.Element("recordlist")
	# if name == '78s':
		
		# with open(src,'r') as f:
		# 	data = "".join(f.readlines()).replace('\r\n','')
		# 	splitter = re.findall(u'<row cid="\d+" Deleted="0">(<DocType>%s</DocType>(?:(?!<\/row>).)*)' % doc_type,data,re.DOTALL)
		# 	for i,el in enumerate(splitter):
		# 		node = etree.fromstring("<record>%s</record>" % el)
		# 		node.set('CID', unicode(i+1))
		# 		element_list.append(node)
		# 		if j == "test" and i > 5000:
		# 			break
		# 	tree = etree.ElementTree(element_list)
		# 	if doc_type in short_names.keys():
		# 		write_name = short_names[doc_type]
		# 	else:
		# 		write_name = doc_type.lower()+'s' 
		# 	if j == "test":
		# 		tree.write("record_groups/itma.recordlist.%s.test.xml"%write_name,encoding='UTF-8',pretty_print=True)
