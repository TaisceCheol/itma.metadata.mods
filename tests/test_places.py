from geopy.geocoders import Nominatim
from SPARQLWrapper import SPARQLWrapper, JSON

geolocator = Nominatim(country_bias='IE')

place = "Willie Clancy Summer School, Miltown Malbay"

place = place[place.index(',')+1:].strip()
location = geolocator.geocode(place)


print location.raw.keys()

# sparql = SPARQLWrapper("http://data.logainm.ie/sparql")
# sparql.setQuery("""
# 		PREFIX log: <http://data.logainm.ie/ontology/>
# 		SELECT DISTINCT *
# 		WHERE {
# 			{
# 				?place log:nonValidatedName "%s"@en
# 			} UNION {
# 				?place foaf:name "%s"@en
# 			}
# 		}
# """ % (location,location))

# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()['results']['bindings'][0]['place']['value']
