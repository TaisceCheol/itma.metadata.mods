import json
from SPARQLWrapper import SPARQLWrapper, JSON

def dbpedia_name_query(name,printResult=False):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")

	sparql.setQuery("""
	    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	   	PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX dbp: <http://dbpedia.org/property/>
		PREFIX dbc: <http://dbpedia.org/category/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		PREFIX dc: <http://purl.org/dc/terms/>
		PREFIX yago: <http://dbpedia.org/class/yago/>
	    SELECT *
	    WHERE { 
	  		?entity foaf:name "%s"@en .
	  		?entity rdfs:label ?name .
	      	?entity rdf:type yago:Artist109812338 .	  		
	      	?entity dbo:abstract ?abstract .
	  		OPTIONAL {
	  			?entity dbo:birthDate ?born .
	  		}	  		
	  		OPTIONAL {
	      		?entity dbo:deathDate ?died
	  		}
	  		filter langMatches(lang(?abstract),"en")    
	  	}
		LIMIT 1
	""" % name)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	if len(results['results']['bindings']):
		if printResult:print json.dumps(results,indent=True)
		data = {}
		for result in results['results']['bindings']:
			for v in results['head']['vars']:
				if v in result.keys():
					data[v] = result[v]
		return data
	else:
		return None


people = ['Martin Hayes','Tommy Potts','Tommy Peoples','Frank Harte']
for p in people:
	print dbpedia_name_query(p)['born']['value']


