import os
from lxml import etree

output_dir = 'test_transform_outputs'

transforms = [os.path.join('xslt_transforms/sound',x) for x in filter(lambda x: not x.startswith('.'),os.listdir('xslt_transforms/sound'))]

transform = etree.XSLT(etree.parse(transforms[0]))

records = "record_groups/itma.recordlist.sounds.test.xml"

record_xml = etree.parse(records).getroot()

material = '78 rpm'

elements = etree.Element("recordlist")

for record in record_xml.iterchildren():
	if record.find("MaterialType").text == material:
		elements.append(record)
		# break

transformed_record = transform(elements)
transformed_record.write(os.path.join(output_dir,'itma.mods.test.%s.xml'% material.replace(' ','')),encoding='UTF-8',pretty_print=True)
print etree.tostring(transformed_record,pretty_print=True)
