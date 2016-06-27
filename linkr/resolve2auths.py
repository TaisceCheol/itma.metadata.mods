# -*- coding: utf-8 -*-
import json,click,subprocess,os,threading
from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import process
from lxml import etree
from multiprocessing.dummy import Pool

class Redstore(threading.Thread):
	"""
	http://stackoverflow.com/questions/984941/python-subprocess-popen-from-a-thread
	"""
	def __init__(self,port):
		self.port = port
		self.stdout = None
		self.stderr = None
		threading.Thread.__init__(self)
	
	def run(self):
		p = subprocess.Popen(('redstore -p %s -b localhost' % self.port).split(),
				shell=False,stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
		self.stdout,self.stderr = p.communicate()

class Resolvr():
	def __init__(self):
		self.start_triplestores()
		self.relators = self.get_relators()
		self.instruments = self.get_instruments()

		self.linked_roles = {}
		self.term_lookup = {}

		self.failed = []

	def link_roles(self,role_file='../itma.roles.xml', output_file='../linked_roles_lookup.json'):
		roles = etree.parse(role_file)
		print 'Linking to authority files'
		roles = roles.xpath('//NamedRole')
		map(self.process_role,roles)
		linked_roles['term_lookup'] = term_lookup

		with open(output_file,'w') as f:
			json.dump(linked_roles,f,indent=True)

	def start_triplestores(self):
		FNULL = open(os.devnull, 'w')
		triple_stores = {}
		triple_stores['lcmpt'] = {'port':'8090','file':'/Users/ITMA/.authorities/authoritiesperformanceMediums.ttl'}
		triple_stores['relators'] = {'port':'8092','file':'/Users/ITMA/.authorities/relators.ttl'}
		print 'Starting triplestores...'
		for item in triple_stores.iteritems():
			print 'starting on port %s' % item[-1]['port']
			x = Redstore(item[-1]['port'])
			x.start()
			subprocess.check_call(["curl",'-T',item[-1]['file'],'-H','Content-Type: application/x-turtle','http://localhost:%s/data/%s' % (item[-1]['port'],item[0])],stdout=FNULL,stderr=FNULL)


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

	def musicbrainz_instrument(self,term):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
				PREFIX wd: <http://www.wikidata.org/entity/> 
				PREFIX wdt: <http://www.wikidata.org/prop/direct/>
			    SELECT ?label ?source ?id ?url
			    WHERE { 
			    	  ?entity rdfs:label "%s"@en .
			    	  ?entity wdt:P1330 ?id .
			    	  wd:P1330 wdt:P1630 ?url .
			    	  wd:P1330 wdt:P1896 ?source .
		""" % term )
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		return results['results']['bindings']

	def musicbrainz_person(self,term):
		sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
		sparql.setQuery("""
			PREFIX wd: <http://www.wikidata.org/entity/> 
			PREFIX wdt: <http://www.wikidata.org/prop/direct/>
		    SELECT *
		    WHERE { 
		    	  ?entity rdfs:label "%s"@en .
		    	  ?entity wdt:P434 ?id .
		    	  wd:P434 wdt:P1630 ?url .
		    	  wd:P434 wdt:P1896 ?source
		    }
		""" % term)
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

	def get_match(self,term):
		if term not in self.linked_roles.keys() and term not in self.failed:
			# check self.relators first
			result = process.extract(term,self.relators,limit=1)
			if len(result) and result[0][-1] > 90:
				if result[0][0] not in self.linked_roles.keys():
					# print term,result[0][0]
					self.linked_roles[result[0][0]] = self.get_single_relator(result[0][0])
					self.term_lookup[term] = result[0][0]
			else:
				# then self.instruments			
				result = process.extract(term,self.instruments,limit=1)
				if len(result) and result[0][-1] > 90:
					if result[0][0] not in self.linked_roles.keys():
						# print term,result[0][0]
						self.linked_roles[result[0][0]] = self.get_single_instrument(result[0][0])
						self.term_lookup[term] = result[0][0]
				else:
					#then getty
					try:
						aat = get_aat_term(term)
					except:
						aat = []
					if len(aat) != 0:
						# print term,aat
						self.linked_roles[term] = aat
						self.term_lookup[term] = result[0][0]
					else:
						# attempt to catch recursively using tokenization
						# if len(term.split()) > 1:
							# print 'Failed to get match for %s. Attempting to recursively match across: %s' % (term,str(term.split()))
						print 'Trying dbpedia for: %s' % term
						for item in self.musicbrainz_instrument(term):
							print item
						# else:
							# self.failed.append(term)
							# print 'Failed to link term: %s' % term	
	
	def process_role(self,el):
		values = el.xpath('Role/text()')
		map(self.get_match,values)
							
# r = Resolvr()
# r.link_roles()

