import glob,shutil
from lxml import etree

MODS = "http://www.loc.gov/mods/v3"

data = glob.glob("mods_records/**.xml")

parsed_data = [etree.parse(x) for x in data]

transform_path = "xslt_transforms/solr/mods2solr.xsl"

transform = etree.XSLT(etree.parse(transform_path))

all_records = etree.Element("{%s}modsCollection"%MODS)

for item in parsed_data:
	records = item.xpath("//mods:mods",namespaces={'mods':MODS})
	for r in records:
		all_records.append(r)
		# if len(all_records) >= 5:break
	# break

transform(all_records).write('sample_solr_import.xml',pretty_print=True)

shutil.copy('sample_solr_import.xml','/Users/itma/code/docker.solr/sample_solr_import.xml')