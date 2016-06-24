import json,click,subprocess	
from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import process
from lxml import etree
from multiprocessing.dummy import Pool

class Resolvr():
	def __init__(self):
		self.start_triplestores()
		
		self.relators = self.get_relators()
		self.instruments = self.get_instruments()

		self.linked_roles = {}
		self.term_lookup = {}

		self.failed = []

	def link_roles(roles, output_file='../linked_roles_lookup.json'):
	#	roles = etree.parse('itma.roles.xml')
		print 'Linking to authority files'
		roles = roles.xpath('//NamedRole')
		map(self.process_role,roles)
		linked_roles['term_lookup'] = term_lookup

		with open(output_file,'w') as f:
			json.dump(linked_roles,f,indent=True)

	def start_triplestores(self):
		print 'Starting triplestores'
		try:
			subprocess.check_call(["nc","-z","localhost","8090"])
		except:
			subprocess.call(['redstore','-p','8090','-b','localhost','-F','turtle','-F','turtle','-f','/Users/ITMA/.authorities/authoritiesperformanceMediums.ttl'])
		try:
			subprocess.check_output(["nc","-z","localhost",'8092'])
		except:
			subprocess.call(['redstore','-p','8090','-b','localhost','-F','turtle','-F','turtle','-f','/Users/ITMA/.authorities/relators.ttl'])
		print 'Triplestores started'

	def get_aat_term(self,item):
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
	def get_instruments(self):
		sparql = SPARQLWrapper("http://localhost:8090/sparql")
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

	def get_single_instrument(self,rel):
		sparql = SPARQLWrapper("http://localhost:8090/sparql")
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

	def get_relators(self):
		sparql = SPARQLWrapper("http://localhost:8092/sparql")
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

	def get_single_relator(self,rel):
		sparql = SPARQLWrapper("http://localhost:8092/sparql")
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

	def process_role(self,el):
		value = el.xpath('Role/text()')
		if len(value):
			value = value[0]
			if value not in self.linked_roles.keys() and value not in self.failed:
				# check self.relators first
				result = process.extract(value,self.relators,limit=1)
				if len(result) and result[0][-1] > 95:
					if result[0][0] not in self.linked_roles.keys():
						# print value,result[0][0]
						self.linked_roles[result[0][0]] = get_single_relator(result[0][0])
						self.term_lookup[value] = result[0][0]
				else:
					# then self.instruments			
					result = process.extract(value,self.instruments,limit=1)
					if len(result) and result[0][-1] > 95:
						if result[0][0] not in self.linked_roles.keys():
							# print value,result[0][0]
							self.linked_roles[result[0][0]] = get_single_instrument(result[0][0])
							self.term_lookup[value] = result[0][0]
					else:
						#then getty
						try:
							aat = get_aat_term(value)
						except:
							aat = []
						if len(aat) != 0:
							# print value,aat
							self.linked_roles[value] = aat
							self.term_lookup[value] = result[0][0]
						else:
							self.failed.append(value)
							print 'Failed to link term: %s' % value								




