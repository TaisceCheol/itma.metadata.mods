import os
from lxml import etree

output_dir = 'test_transform_outputs'

transforms = [os.path.join('xslt_transforms/audio',x) for x in filter(lambda x: not x.startswith('.'),os.listdir('xslt_transforms/audio'))]

transform = etree.XSLT(etree.parse(transforms[0]))

records = "record_groups/audio/itma.78s.xml"

record_xml = etree.parse(records).getroot()

elements = etree.Element("recordlist")

for record in record_xml.iterchildren():
	elements.append(record)

transformed_record = transform(elements)
transformed_record.write(os.path.join(output_dir,'itma.mods.test.78s.xml'),encoding='UTF-8',pretty_print=True)
# print etree.tostring(transformed_record,pretty_print=True)
