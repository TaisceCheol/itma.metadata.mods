import os
from lxml import etree

output_dir = 'test_transform_outputs'

transforms = [os.path.join('xslt_transforms/audio',x) for x in filter(lambda x: not x.startswith('.'),os.listdir('xslt_transforms/audio'))]

print transforms

transform = etree.XSLT(etree.parse(transforms[-1]))

carrier = 'LP'

records = "record_groups/audio/itma.%s.xml" % carrier

record_xml = etree.parse(records).getroot()

elements = etree.Element("recordlist")

for i,record in enumerate(record_xml.iterchildren()):
	elements.append(record)
	if i > 25:break

transformed_record = transform(elements)
transformed_record.write(os.path.join(output_dir,'itma.mods.test.%s.xml') % carrier,encoding='UTF-8',pretty_print=True)
