import json,click
from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import process
from lxml import etree

def get_carriers():
	sparql = SPARQLWrapper("http://localhost:8095/sparql")
	sparql.setQuery("""
		PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	    SELECT ?entity ?label
	    WHERE { 
	    	?entity skos:prefLabel ?label .
			# FILTER (langMatches(lang(?label),'en'))
	    }
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return [x['label']['value'] for x in results['results']['bindings']]

def get_single_carrier(carrier):
	sparql = SPARQLWrapper("http://localhost:8095/sparql")
	sparql.setQuery("""
		PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	    SELECT ?entity
	    WHERE { 
	    	?entity skos:prefLabel "%s"@en
	    }
	    LIMIT 1
	""" % carrier)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings'][0]

def get_aat_term(item):
	sparql = SPARQLWrapper("http://localhost:8097/sparql")
	sparql.setQuery("""
		#don't need prefixes for online?
	    SELECT ?label ?entity ?source
	    WHERE { 
			?entity a skos:Concept ;
				skos:inScheme ?source ;
				rdfs:label "%s"@en ;
				gvp:prefLabelGVP ?prefterm	.
			?prefterm gvp:term ?label			
	    }
	""" % item)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings']

def get_aat_term(item):
	sparql = SPARQLWrapper("http://vocab.getty.edu/sparql")
	sparql.setQuery("""
		#don't need prefixes for online?
	    SELECT ?label ?entity ?source
	    WHERE { 
			?entity a skos:Concept ;
				skos:inScheme ?source ;
				rdfs:label "%s"@en ;
				gvp:prefLabelGVP ?prefterm	.
			?prefterm gvp:term ?label			
	    }
	""" % item)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings']

# requires brew install redstore
def get_instruments():
	sparql = SPARQLWrapper("http://localhost:8080/sparql")
	sparql.setQuery("""
		PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
		PREFIX identifiers: <http://id.loc.gov/vocabulary/identifiers/>
	    SELECT ?instrument
	    WHERE { 
			?object madsrdf:authoritativeLabel ?instrument
	    	# ?object identifiers:lccn ?lcid .
	    	# ?object madsrdf:hasSource ?hasSource .
	    	# ?hasSource madsrdf:citation-note ?citation .
	    	# ?hasSource madsrdf:citation-source ?source
	    }
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return [x['instrument']['value'] for x in results['results']['bindings']]

def get_single_instrument(rel):
	sparql = SPARQLWrapper("http://localhost:8080/sparql")
	sparql.setQuery("""
		PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
		PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 		
	    SELECT ?entity ?label ?source
	    WHERE { 
			?entity madsrdf:authoritativeLabel "%s"@en ;
					madsrdf:authoritativeLabel ?label ;
					skos:inScheme ?source ;

	    }
	    LIMIT 1
	""" % rel)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings'][0]

def get_relators():
	sparql = SPARQLWrapper("http://localhost:8090/sparql")
	sparql.setQuery("""
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
	    SELECT ?relator
	    WHERE { 
			?entity madsrdf:authoritativeLabel ?relator
	    }
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return [x['relator']['value'] for x in results['results']['bindings']]

def get_single_relator(rel):
	sparql = SPARQLWrapper("http://localhost:8090/sparql")
	sparql.setQuery("""
		PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
	    SELECT ?entity ?code ?label ?source
	    WHERE { 
			?entity madsrdf:authoritativeLabel "%s"@en ;
					madsrdf:code ?code ;
					madsrdf:authoritativeLabel ?label ;
					madsrdf:isMemberOfMADSScheme ?source

	    }
	    LIMIT 1
	""" % rel)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings'][0]

relators = get_relators()

instruments = get_instruments()

roles = etree.parse('itma.roles.xml')

linked_roles = {}

term_lookup = {}

failed = []

with click.progressbar(roles.xpath('//NamedRole'),label="Linking to authority files...") as bar:
	for i,el in enumerate(bar):
		value = el.xpath('Role/text()')
		if len(value):
			value = value[0]
			if value not in linked_roles.keys() and value not in failed:
				# check relators first
				result = process.extract(value,relators,limit=1)
				if len(result) and result[0][-1] > 95:
					if result[0][0] not in linked_roles.keys():
						# print value,result[0][0]
						linked_roles[result[0][0]] = get_single_relator(result[0][0])
						term_lookup[value] = result[0][0]
				else:
					# then instruments			
					result = process.extract(value,instruments,limit=1)
					if len(result) and result[0][-1] > 95:
						if result[0][0] not in linked_roles.keys():
							# print value,result[0][0]
							linked_roles[result[0][0]] = get_single_instrument(result[0][0])
							term_lookup[value] = result[0][0]
					else:
						#then getty
						# try:
							aat = get_aat_term(value)
							if len(aat) != 0:
								# print value,aat
								linked_roles[value] = aat
								term_lookup[value] = result[0][0]
							else:
								failed.append(value)
								print 'Failed to link term: %s' % value								
						# except:
							# failed.append(value)
							# print 'Failed to link term: %s' % value
		if i > 250:
			quit()

linked_roles['term_lookup'] = term_lookup

with open("linked_roles_lookup.json",'w') as f:
	json.dump(linked_roles,f,indent=True)

