import json
from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree

# requires brew install redstore

def get_instrument_data(instrument):
	global sparql
	sparql.setQuery("""
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
		PREFIX identifiers: <http://id.loc.gov/vocabulary/identifiers/>
		PREFIX ri: <http://id.loc.gov/ontologies/RecordInfo#>
		PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
		PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
		PREFIX cs: <http://purl.org/vocab/changeset/schema#>
	    SELECT ?object ?lcid ?citation ?source
	    WHERE { 
			?object madsrdf:authoritativeLabel "%s"@en .
	    	?object identifiers:lccn ?lcid .
	    	?object madsrdf:hasSource ?hasSource .
	    	?hasSource madsrdf:citation-note ?citation .
	    	?hasSource madsrdf:citation-source ?source
	    }
	    LIMIT 1
	""" % instrument)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	if len(results['results']['bindings']):
		return results['results']['bindings']
	else:
		return None

sparql = SPARQLWrapper("http://localhost:8080/sparql")

for i in get_instrument_data('piano'):
	print "Citation:%s\nSource:%s\nURL:%s" % (i['citation']['value'],i['source']['value'],i['object']['value'])

# roles = list(set(etree.parse('itma.roles.xml').xpath('/NamedRoles/NamedRole/Role/text()')))

# for role in roles:
# 	try:
# 		for i in get_instrument_data(role.rstrip('s')):
# 			print "Citation:%s\nSource:%s\nURL:%s" % (i['citation']['value'],i['source']['value'],i['object']['value'])
# 	except:
# 		print 'Could not find data for term: %s' % role
