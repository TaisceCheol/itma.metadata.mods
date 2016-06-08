import json
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:8080/sparql")

sparql.setQuery("""
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
	PREFIX identifiers: <http://id.loc.gov/vocabulary/identifiers/>
	PREFIX ri: <http://id.loc.gov/ontologies/RecordInfo#>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
	PREFIX cs: <http://purl.org/vocab/changeset/schema#>
    SELECT ?object
    WHERE { ?object identifiers:lccn "mp2013015001" }
    LIMIT 1
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
if len(results['results']['bindings']):
	print results