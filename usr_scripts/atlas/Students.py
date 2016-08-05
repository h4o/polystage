import csv

from python.atlas import Users, Groups
from python.atlas.User import Student
from python.scripts.Runner import ReversibleRunner

from python.schema import yaml_loader


def load_students_file(user_file):
    config = yaml_loader.load_file(user_file)
    users = []
    with open(config['csv_file']) as f:
        users_csv = csv.reader(f, delimiter=';')
        for row in users_csv:
            user = Student(row)
            users.append(user)
    return {'users': users, 'groups': config['groups']}


def remove_students(user_file):
    students = load_students_file(user_file)
    for student in students:
        Users.Remove(student)


def load(user_file='schema/import_user.yml'):
    script = ReversibleRunner()
    data = load_students_file(user_file)
    students, groups = data['users'], data['groups']
    group_names = script.do(Groups.GetAll())
    group_names = [group['name'] for group in group_names]
    for group in groups:
        group in group_names or script.do(Groups.Create(group))

    for student in students:
        script.do(Users.Create(student))
        for group in groups:
            script.do(Users.AddToGroup(student.username, group), never_undo=True)

    return script
