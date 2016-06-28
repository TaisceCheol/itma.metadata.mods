# -*- encoding: UTF-8 -*-
import redis,json
from geopy.geocoders import Nominatim
from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree

class PlaceR():
	def __init__(self,records,output_file,unmatched):
		self.redis_cache = redis.StrictRedis(host='localhost',port=6379,db=0)
		self.geolocator = Nominatim()
		self.cache = {}
		self.placelist = etree.Element("Locations")
		self.logainm_links = {}
		self.unmatched = []
		places = []
		[[places.append(y.text) for y in x.xpath('*[self::CreationLocation or self::GeographicalLocation]')] for x in records]
		map(self.locate,places)
		map(self.link_to_logainm,self.cache.values())
		map(self.link_to_record,records)

		etree.ElementTree(self.placelist).write(output_file,pretty_print=True)

		with open(unmatched,'w') as f:
			for item in self.unmatched:
				f.write(item+'\n')

	def create_xml_nodes(self,record,field):
		for item in record.xpath(field):
			place = item.text
			if place in self.redis_cache.keys():
				location = json.loads(self.redis_cache.get(place))
				el = etree.Element('Location',catid=record.attrib['CID'],type=field.lower())
				el.text = place
				for key,value in location.raw.iteritems():
					el.attrib[key] = unicode(value)
				if place.split(',')[0] in self.logainm_links.keys():
					el.attrib['logainm'] = self.logainm_links[place.split(',')[0]]
				self.placelist.append(el)		

	def link_to_record(self,record):
		for field in ['GeographicalLocation','CreationLocation']:
			self.create_xml_nodes(record,field)

	def link_to_logainm(self,place):
		place = place.address.split(',')[0]
		if place not in self.logainm_links.keys():
			sparql = SPARQLWrapper("http://data.logainm.ie/sparql")
			sparql.setQuery("""
					PREFIX log: <http://data.logainm.ie/ontology/>
					SELECT DISTINCT *
					WHERE {
						{
							?place log:nonValidatedName "%s"@en
						} UNION {
							?place foaf:name "%s"@en
						}
					}
			""" % (place,place))
			sparql.setReturnFormat(JSON)
			result = sparql.query().convert()['results']['bindings']
			for item in result:
				self.logainm_links[place] = item['place']['value']

	def locate(self,place):
		if place not in self.redis_cache.keys():
			location = self.geolocator.geocode(place)
			if location != None:
				location = json.dumps(location)
				self.redis_cache.set(place,location)
			else:
				if len(place.split(',')) > 1:
					second_order_place = place[place.index(',')+1:].strip()
					if second_order_place not in self.redis_cache.keys():
						# remove possible event name from place string and try once more to geocode
						location = self.geolocator.geocode(second_order_place)
						if location != None:
							location = json.dumps(location)
							self.redis_cache.set(place,location)
					else:
						self.redis_cache.set(place,self.redis_cache.get(second_order_place))
				else:
					print "Place could not be found: '%s'" % place
		return None
	
