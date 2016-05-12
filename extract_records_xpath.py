from lxml import etree
from rdflib import Graph,URIRef

class MaterialTypes:
	listall = {}
	def __init__(self):
		self.src = "itma.cat.soutron_20160216.xml"
		self.data = etree.parse(self.src)
		self.xpath = "/recordlist/record[DocType[text()='%s']]/MaterialType/text()"
		self.types = {'sound':'Sound Recording','print':'Printed Material','image':'Image','video':'Video'}
		for key,value in self.types.iteritems():
			self.listall[key] = self.get(value)
	def get(self,q):
		return sorted(set(self.data.xpath(self.xpath % q)))

material = MaterialTypes()

print material.listall['video']
