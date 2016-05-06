import glob
from lxml import etree

data = glob.glob("test_transform_outputs/**.xml")

parsed_data = [etree.parse(x) for x in data[4:5]]

transform_path = "xslt_transforms/solr/mods2solr.xsl"

transform = etree.XSLT(etree.parse(transform_path))

for item in parsed_data[0:]:
	# print etree.tostring(item)
	# print etree.tostring(transform(item),pretty_print=True)
	transform(item).write('sample_solr_import.xml',pretty_print=True)
	break