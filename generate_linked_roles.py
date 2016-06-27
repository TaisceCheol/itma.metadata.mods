from lxml import etree
from linkr import link2catalog,resolve2auths,role_extractor,map_roles,place_extractor

# PATHS
soutron_cat = 'itma.cat.soutron_20160216.xml'
role_path = 'itma.roles.xml'
place_path = 'itma.places.xml'
roles_lookup_path = 'linked_roles_lookup.json'
linked_role_path = 'itma.roles.linked.xml'
linked_cat_path = 'itma.cat.linked.xml'

################################################
## Pipeline Extract -> Resolve -> Map -> Link ##
################################################

n_records = 100

records = etree.parse(soutron_cat).xpath('/recordlist/record')[0:n_records]

print '::Extracting...'
role_extractor.Extract(records,role_path)
print '::Geolocating'
place_extractor.PlaceR(records,place_path)
# print '::Resolving'
# r = resolve2auths.Resolvr()
# r.link_roles(role_path,roles_lookup_path)
# print '::Mapping'
# map_roles.MapR(role_path,roles_lookup_path,linked_role_path)
# print '::Linking'
# link2catalog.Link(records,linked_role_path,linked_cat_path)

