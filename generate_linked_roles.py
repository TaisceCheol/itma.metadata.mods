from lxml import etree
from linkr import link2catalog,resolve2auths,role_extractor,map_roles,place_extractor,resolve_materials
from random import shuffle,seed
# PATHS
soutron_cat = 'data_inputs/itma.cat.soutron_20160216.xml'
role_path = 'data_outputs/itma.roles.xml'
place_path = 'data_outputs/itma.places.xml'
unmatched_names = 'data_outputs/itma.unmatched.places.txt'
roles_lookup_path = 'data_outputs/linked_roles_lookup.json'
names_lookup_path = 'data_outputs/linked_names_lookup.json'
materials_lookup_path = 'data_outputs/material_lookup.json'
linked_role_path = 'data_outputs/itma.roles.linked.xml'
linked_cat_path = 'data_outputs/itma.cat.linked.xml'

################################################
## Pipeline Extract -> Resolve -> Map -> Link ##
################################################

n_records = 10
offset = 0

records = filter(lambda x:x.xpath('DocType')[0].text != 'Copy',etree.parse(soutron_cat).xpath('/recordlist/record'))
seed(10001)
shuffle(records)

records = records[offset:offset+n_records]

print '::Extracting...'
role_extractor.Extract(records,role_path)
print '::Geolocating'
place_extractor.PlaceR(records,place_path,unmatched_names)
print '::Resolving'
r = resolve2auths.Resolvr()
r.link_roles(role_path,roles_lookup_path,names_lookup_path)
print '::Mapping'
map_roles.MapR(role_path,roles_lookup_path,names_lookup_path,linked_role_path)
print '::Linking'
link2catalog.Link(records,linked_role_path,linked_cat_path,place_path,materials_lookup_path)

