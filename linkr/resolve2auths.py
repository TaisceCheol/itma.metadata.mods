	# -*- coding: utf-8 -*-
import json,click,subprocess,os,threading,time,urllib2,redis
from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import process
from lxml import etree
from multiprocessing.dummy import Pool
from itertools import repeat 

class Redstore(threading.Thread):
	"""
	http://stackoverflow.com/questions/984941/python-subprocess-popen-from-a-thread
	"""
	def __init__(self,port):
		self.port = port
		self.stdout = None
		self.stderr = None
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		p = subprocess.Popen(('redstore -p %s -b localhost' % self.port).split(),
				shell=False,stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
		self.stdout,self.stderr = p.communicate()

class Resolvr():
	def __init__(self,autostart=True):
		if autostart == True:
			self.start_triplestores()
			self.relators = self.get_relators()
			self.instruments = self.get_instruments()
		self.redis_roles_cache = redis.StrictRedis(host='localhost',port=6379,db=1)
		self.redis_lookup_cache = redis.StrictRedis(host='localhost',port=6379,db=2)
		self.vocal = ['tenor','baritone','soprano','alto','contralto']
		self.linked_roles = {}
		self.term_lookup = {}
		self.failed = []

	def link_roles(self,role_file='../itma.roles.xml', output_file_roles='../data_outputs/linked_roles_lookup.json',output_file_names='../data_outputs/linked_names_lookup.json'):
		roles = etree.parse(role_file)
	 	names = roles.xpath('//NamedRole/Name/text()')	
		print 'Linking to authority files'
		roles = roles.xpath('//NamedRole')
		map(self.process_role,roles)
	 	self.linked_roles['term_lookup'] = self.term_lookup
	 	viaf_records = filter(lambda x: x != None,map(self.link_name,names))
	 	linked_name_store = {}
	 	for entry in viaf_records:
	 		linked_name_store[entry[0]] = entry[-1]
		with open(output_file_roles,'w') as f:
			json.dump(self.linked_roles,f,indent=True)
	 	with open(output_file_names,'w') as f:
	 		json.dump(linked_name_store,f,indent=True)

	def start_triplestores(self):
		FNULL = open(os.devnull, 'w')
		triple_stores = {}
		triple_stores['lcmpt'] = {'port':'8090','file':'/Users/ITMA/.authorities/authoritiesperformanceMediums.ttl'}
		triple_stores['relators'] = {'port':'8092','file':'/Users/ITMA/.authorities/relators.ttl'}
		triple_stores['carriers'] = {'port':'8096','file':'/Users/ITMA/.authorities/es_carriers.rdf'}

		print 'Starting triplestores...'
		for item in triple_stores.iteritems():
			print 'starting on port %s' % item[-1]['port']
			x = Redstore(item[-1]['port'])
			x.start()
			time.sleep(0.25)
			subprocess.check_call(["curl",'-T',item[-1]['file'],'http://localhost:%s/data/%s' % (item[-1]['port'],item[0])],stdout=FNULL,stderr=FNULL)


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
			    	  wd:P1330 wdt:P1896 ?source  
			}
		""" % term.title() )
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
		print rel
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

	def get_match(self,term,record_type):
		if term not in self.linked_roles:
			check_inst = process.extract(term,self.instruments,limit=1)
			if check_inst[0][-1] > 90:
				if record_type == 'Sound Recording':
					role = 'Performer'
				else:
					role = 'Creator'
				term = check_inst[0][0] 
			else:
				# next check if in relators
				check_relators = process.extract(term,self.relators,limit=1)
				if check_relators[0][-1] > 90:
					role = check_relators[0][0]
				else:
					if record_type == 'Sound Recording':
						role = 'Performer'
					else:
						role = 'Creator'
			self.linked_roles[term] = self.get_single_relator(role)


	def process_role(self,el):
		values = el.xpath('Role/text()')
		record_type = el.xpath('DocType')[0].text
		map(self.get_match,values,repeat(record_type,len(values)))
	
	def has_musicbrainz_id(self,term):
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

	def link_name(self,query):
		viafid = None
		baseurl = "http://www.viaf.org/viaf/AutoSuggest?query="
		try:
			response = urllib2.urlopen(baseurl + urllib2.quote(query.decode('UTF-8')))
			data = json.load(response)

			matches = set()

			if data['result']:
				for r in data['result']:
					if int(r['score']) > 1000:
						matches.add(r['viafid'])

			if len(matches) > 1:
				for item in matches:
					result = self.has_musicbrainz_id(item)
					if len(result):
						viafid = item
			elif len(list(matches)):
				viafid = list(matches)[0]

			if viafid:
				return [query,"https://viaf.org/viaf/%s" % viafid]
			else:
				return None		
		except:
			return None					
# r = Resolvr()
# r.link_roles()

