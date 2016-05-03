from lxml import etree
import re,subprocess

regexpNS = "http://exslt.org/regular-expressions"

def parse_materials(tree):
	types = ['Sound Recording','Image','Printed Material','Serial Issue','Video','Copy']
	short_names = {'Sound Recording':'audio','Printed Material':'printed','Serial Issue':'serial','Copy':'copy','Image':'image','Video':'video'}
	data = {}
	for t in types:
		print t
		data[short_names[t]] = tree.xpath("/recordlist/record[DocType/text() = '%s']" % t)
	return data

def parse_audio_carriers(tree,carrier):
	audio_carriers = {}
	carriers = {}
	carriers['CYL'] = ["Sound Cylinder"]
	carriers['GALVANO'] = ["Galvanoplastic"]
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
	# for item in carriers.iteritems():
	starts_with_strings = " or ".join(['MaterialType[starts-with(text(),\'%s\')]'%x for x in carriers[carrier]])
	# audio_carriers[carrier] = tree.xpath('/recordlist/record[%s]' % starts_with_strings)
	return tree.xpath('/recordlist/record[%s]' % starts_with_strings)

src = "itma.cat.soutron_20160216.xml"

tree = etree.parse(src)

element_list = etree.Element("recordlist")

data = [element_list.append(x) for x in parse_audio_carriers(tree,'78')]

etree.ElementTree(element_list).write('record_groups/audio/itma.78s.xml',pretty_print = True,encoding='UTF-8')

# print tree.xpath("/recordlist/record[MaterialType[starts-with(text(),'ADAT')] or MaterialType[starts-with(text(),'DAT')]]")

# materials = parse_materials(tree)

# parse_audio_carriers(materials['audio'])

# all_carriers = sorted(set(tree.xpath("/recordlist/record/MaterialType/text()")))

# for c in all_carriers:
# 	print c

# print len(all_carriers)


