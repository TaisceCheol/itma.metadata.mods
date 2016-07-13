from lxml import etree

transform = etree.XSLT(etree.parse('xslt_transforms/basic_mods.transform.xsl'))

soutron_data = etree.parse('itma.cat.soutron_20160216.xml')

mods_records = etree.Element("modslist")

for record in soutron_data.xpath('/recordlist/record'):
	tr = transform(record)
#	print etree.tostring(tr,pretty_print=True)
	break

#etree.ElementTree(mods_records).write('sample.mods.xml',pretty_print=True)

