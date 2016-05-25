import os,glob,re
from lxml import etree

output_dir = 'mods_records'

carriers = filter(lambda x: x.find('solr') == -1,[x for x in glob.glob("xslt_transforms/**/**")])

carriers = [re.match('^(?P<full>.*\/(?P<category>\w+)/itma\.transform\.(?P<media>\w+)\.xsl)$',x).groupdict() for x in carriers]

for carrier in carriers:
	transform = etree.XSLT(etree.parse(carrier['full']))
	records = "record_groups/%s/itma.%s.xml" % (carrier['category'],carrier['media'])
	try:
		record_xml = etree.parse(records).getroot()

		elements = etree.Element("recordlist")

		for i,record in enumerate(record_xml.iterchildren()):
			elements.append(record)
			# if i == 99:break

		transformed_record = transform(elements)
		transformed_record.write(os.path.join(output_dir,'itma.mods.test.%s.xml') % carrier['media'],encoding='UTF-8',pretty_print=True)
	except:
		print 'No record exists for %s => %s' % (carrier['category'],carrier['media'])
