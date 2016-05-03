from lxml import etree
import re,subprocess

src = "ITMA-catalogue_20160216.xml"
xslt_src = "soutron2mods.xsl"

DOWHAT = 'WRITE'

transform = etree.XSLT(etree.parse(xslt_src))
if DOWHAT == 'WRITE':
	element_list = etree.Element("recordlist")
	tag_list = set()
	last_mtype = None
	n_items = 5
	counter = 0
	with open(src,'r') as f:
		data = "".join(f.readlines()).replace('\r\n','')
		splitter = re.findall(u'<row cid="\d+" Deleted="0">((?:(?!<\/row>).)*)',data,re.DOTALL)
		for i,el in enumerate(splitter):
			node = etree.fromstring("<record>%s</record>" % el)
			node.set('CID', unicode(i+1))
			[tag_list.add(x.tag) for x in node.getchildren()]
			mtype = node.getchildren()[0].text
			if counter < n_items:
				element_list.append(node)
			elif mtype != last_mtype and i > n_items:
				print 'New mtype: %s' % mtype
				counter = 0
			last_mtype = mtype
			counter += 1
		tree = etree.ElementTree(element_list)
		print etree.tostring(tree)
		# tree.write("itma.recordlist.xml",encoding='UTF-8',pretty_print=True)
else:
	tree = etree.parse("itma.recordlist.xml")

xtree = transform(tree)
xtree.write("itma.recordlist.mods.xml",encoding='UTF-8',pretty_print=True)
