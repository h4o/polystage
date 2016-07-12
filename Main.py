import json

import Groups
import Projects
import Roles
import Users

# Groups.delete(['4a-2015'])
# Users.remove_students('students.csv')
# Users.import_students('students.csv', ['jira-software-users', 'Les zouzous du dimanche'], create_groups=True)
# Users.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)

# Projects.create('GL', 'Le gang des lover', 'mosser')
# Projects.import_projects('schema/project_sample.yml')
from Requester import req

r = req.get('jira', 'permissionscheme/{}'.format(10000))
print(r)
print(json.dumps(r))
# print(r['permissions'][0]['holder'])
# for a in r['permissions']:
#     print(a['permission'], '=>', a['holder'])


# from Requester import req
#
# r = req.get('jira', 'permissions')['permissions']
# max = (max([len(a) for a in r.keys()]))
# for p in r.values():
#     print('{:.^{max}} => {}'.format(p['key'], p['description'], max=max))


# Roles.create('Les marcheurs en forêt', 'Des arbes, des arbes et encore des arbres')
# d = delete('developers')
# print(d)
# name = 'Les poids lourds de l\'amour'
# r = create(name, 'Brrr... so scared')
# # print(r['id'])
# t = get(name)
# print(t['id'])

