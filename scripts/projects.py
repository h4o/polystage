from atlas import Projects
from schema.yaml_loader import load
from scripts.Scripts import ReversibleRunner
from util.util import pp


def load_multi_project_file(file_name):
    file = load(file_name, 'schema/new_project_template.yml')
    params = file['params']
    params['type'] = params.get('type', 'software')
    params['readers'] = params.get('readers', [])
    params['applink'] = params.get('applink', False)
    params['repositories'] = params.get('repositories', [])
    for project in file['projects']:
        project['key'] = params['tag'] + project['id']
        project['name'] = project.get('name', project['key'])
        project['lead'] = project.get('lead', project['developers'][0])
        project['supervisors'] = set(params['supervisors'] + project.get('supervisors', []))
        project['readers'] = set(params['readers'] + project.get('readers', []))
    return file


def create_multi_project(file_name):
    data = load_multi_project_file(file_name)
    params = data['params']
    script = ReversibleRunner()
    for p in data['projects']:
        script.do(Projects.CreateJira(p['key'], p['name'], p['lead'], project_type=params['type']))
