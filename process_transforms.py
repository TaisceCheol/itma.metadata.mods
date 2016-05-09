import os
from lxml import etree

def get_transform(carrier):
	transform_path = 'xslt_transforms/print/itma.transform.%s.xsl' % carrier
	return etree.XSLT(etree.parse(transform_path))

output_dir = 'test_transform_outputs'

# for carrier in  ['CYL','78','GAL','ACE','LP','REEL','CS','CD','DAT','WAV','MP3','FLAC']:
for carrier in ['BK']:
	transform = get_transform(carrier)

	records = "record_groups/prints/itma.%s.xml" % carrier

	record_xml = etree.parse(records).getroot()

	elements = etree.Element("recordlist")

	for i,record in enumerate(record_xml.iterchildren()):
		elements.append(record)
		if i == 2:	break

	transformed_record = transform(elements)
	transformed_record.write(os.path.join(output_dir,'itma.mods.test.%s.xml') % carrier,encoding='UTF-8',pretty_print=True)
