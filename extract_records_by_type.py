import re,subprocess
from lxml import etree
from dateutil.parser import parse as parse_date
from datetime import date

def parse_materials(tree):
	types = ['Sound Recording','Image','Printed Material','Serial Issue','Video','Copy']
	short_names = {'Sound Recording':'audio','Printed Material':'printed','Serial Issue':'serial','Copy':'copy','Image':'image','Video':'video'}
	data = {}
	for t in types:
		print t
		data[short_names[t]] = tree.xpath("/recordlist/record[DocType/text() = '%s']" % t)
	return data

def process_date_fields(record):
	'''format dates to ISO-8601 subset w3cdtf where possible'''
	date_fields = ['CreationDate','PublicationDate','AccessionDate','CreatedDate']
	matches = []
	for field in date_fields:
		[matches.append(x) for x in record.xpath('%s'%field)]
	for el in matches:
		if el.text:
			try:
				if el.text.find('[') != -1 or el.text.find(']') != -1:
					el.attrib['qualifier'] = 'inferred'
				date_string = parse_date(el.text.lstrip('[').rstrip(']')) 
				date_string = date.isoformat(date_string)
				el.attrib['encoding'] = 'w3cdtf'
				el.text = date_string
			except:
				date_string = el.text
		else:
			data = el.attrib
			if data['nodate'] == '0':
				if data['circa'] == '1':
					el.attrib['qualifier'] = 'inferred'
				date_string = "%s-%s-%s" % (data.get('start_year',''),data.get('start_month',''),data.get('start_day',''))
				date_string = parse_date(date_string)
				date_string = date.isoformat(date_string)
				el.attrib['encoding'] = 'w3cdtf'
				el.text = date_string

def parse_audio_carriers(tree,carrier):
	audio_carriers = {}
	carriers = {}
	carriers['CYL'] = ["Sound Cylinder"]
	carriers['GAL'] = ["Galvanoplastic"]
	carriers['ACE'] = ["Acetate"]
	carriers['78'] = ["78"]
	carriers['LP'] = ["LP",'45']
	carriers['SP'] = ["SP"]
	carriers['EP'] = ["EP","Vinyl EPS"]
	carriers['REEL'] = ["Reel",'reel']
	carriers['CD'] = ["Enhanced Compact","Compact","Compact Disc",'Audio CD']
	carriers['CS'] = ["Audio Cassette","Audio  Cassette","Cassette",'Audio Casette','1 sound cassette']
	carriers['DAT'] = ["DAT","ADAT"]
	carriers['MD'] = ["MiniDisc"]
	carriers['AIFF'] = ['AIFF']
	carriers['WAV'] = ["WAV","Audio file"]
	carriers['MP3'] = ["MP3"]
	carriers['FLAC'] = ["FLAC"]
	starts_with_strings = " or ".join(['MaterialType[starts-with(text(),\'%s\')]'%x for x in carriers[carrier]])
	element_list = etree.Element("recordlist")
	audio_elements = tree.xpath("/recordlist/record[DocType[text() = 'Sound Recording']]")
	[element_list.append(x) for x in audio_elements]
	return etree.ElementTree(element_list).xpath("/recordlist/record[%s]" % starts_with_strings)

src = "itma.cat.soutron_20160216.xml"

tree = etree.parse(src)

element_list = etree.Element("recordlist")

carrier = 'ACE'

data = parse_audio_carriers(tree,carrier)

data = sorted(data,key=lambda x:int(x.get("CID")))

[process_date_fields(x) for x in data]

[element_list.append(x) for x in data]

etree.ElementTree(element_list).write('record_groups/audio/itma.%s.xml' % carrier,pretty_print = True,encoding='UTF-8')



