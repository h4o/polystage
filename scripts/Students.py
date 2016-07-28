import csv
from atlas import Users, Groups
from atlas.User import Student
from scripts.Runner import ReversibleRunner


def load_students(user_file):
    users = []
    with open(user_file) as f:
        users_csv = csv.reader(f, delimiter=';')
        for row in users_csv:
            user = Student(row)
            users.append(user)
    return users


def remove_students(user_file):
    students = load_students(user_file)
    for student in students:
        Users.Remove(student)


def import_students(user_file, groups):
    s = ReversibleRunner()
    students = load_students(user_file)
    group_names = s.do(Groups.GetAll())
    group_names = [a['name'] for a in group_names]
    for group in groups:
        group in group_names or s.do(Groups.Create(group))

    for student in students:
        s.do(Users.Create(student))
        for group in groups:
            s.do(Users.AddToGroup(student.username, group), never_undo=True)

    return s
