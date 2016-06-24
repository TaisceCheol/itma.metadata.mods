# from linkr import role_extractor,resolve2auths,link_roles
from linkr import link2catalog,resolve2auths,role_extractor,map_roles

soutron_cat = 'itma.cat.soutron_20160216.xml'
role_path = 'itma.roles.xml'
roles_lookup_path = 'linked_roles_lookup.json'
linked_role_path = 'itma.roles.linked.xml'
linked_cat_path = 'itma.cat.linked.xml'

#Pipeline Extract -> Resolve -> Map -> Link

role_extractor.Extract(soutron_cat,role_path)
r = resolve2auths.Resolvr()
r.link_roles(role_path,roles_lookup_path)
map_roles.MapR(role_path,roles_lookup_path,linked_role_path)
link2catalog.Link(soutron_cat,linked_role_path,linked_cat_path)

