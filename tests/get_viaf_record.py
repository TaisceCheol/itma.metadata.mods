import urllib2,json
from SPARQLWrapper import SPARQLWrapper, JSON

def has_musicbrainz_id(term):
	sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
	sparql.setQuery("""
		PREFIX wd: <http://www.wikidata.org/entity/> 
		PREFIX wdt: <http://www.wikidata.org/prop/direct/>
	    SELECT *
	    WHERE { 
	    	  ?entity wdt:P214 "%s" ;
	    	  		wdt:P434 ?musicbrainzid
	    }
	""" % term)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings']

def link_name(query):
	viafid = None
	baseurl = "http://www.viaf.org/viaf/AutoSuggest?query="
	response = urllib2.urlopen(baseurl + urllib2.quote(query))
	data = json.load(response)

	matches = set()

	if data['result']:
		for r in data['result']:
			if int(r['score']) > 1000:
				matches.add(r['viafid'])

	if len(matches) > 1:
		for item in matches:
			result = has_musicbrainz_id(item)
			if len(result):
				viafid = item
	elif len(list(matches)):
		viafid = list(matches)[0]

	if viafid:
		return "https://viaf.org/viaf/%s" % viafid
	else:
		return viafid

