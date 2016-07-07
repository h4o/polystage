import csv
import requests
from Requester import req


class Student:
    def __init__(self, row):
        self.year = row[0]
        self.lastname = row[1]
        self.firstname = row[2]
        self.unice_id = row[3]
        self.unice_email = row[4]
        self.mystery_field = row[5]
        self.ine = row[7]

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def __str__(self):
        return 'Yo ! My name is {}, i\'m a student of {}'.format(self.fullname, self.year)

    def get_crowd_format(self):
        user = {
            'name': self.unice_id,
            'first-name': self.firstname,
            'last-name': self.lastname,
            'display-name': '{}'.format(self.fullname),
            'email': self.unice_email,
            'password': {
                'value': 'password'
            },
            'active': True
        }
        return user


def load_students(user_file):
    users = []
    with open(user_file) as f:
        users_csv = csv.reader(f, delimiter=';')
        for row in users_csv:
            user = Student(row)
            users.append(user)
    return users


def get_registered_usernames():
    students = req.get('crowd', 'search', params={'entity-type': 'user'})['users']
    return [s['name'] for s in students]


def get_groups():
    groups = req.get('crowd', 'search', params={'entity-type': 'group'})['groups']
    return [s['name'] for s in groups]


def register_students(user_file, groups):
    students = load_students(user_file)
    _student_insertion(students)
    _group_assignation(students, groups)


def _student_insertion(students):
    for student in students:
        try:
            req.post('crowd', 'user', json=student.get_crowd_format())
            print('The student {} has been registered'.format(student.fullname))
        except requests.exceptions.HTTPError as e:
            print('Could not register {}'.format(student.fullname))
            reason = {
                400: 'Malformed request or the username {}: {} already exists'.format(student.unice_id,
                                                                                      student.fullname),
                403: 'The application is not allowed to create user {}'.format(student.fullname)
            }.get(e.response.status_code, str(e))
            print('Reason: {}'.format(reason))


def _group_assignation(students, groups):
    existing_groups = get_groups()
    for group in groups:
        if group not in existing_groups:
            print('The group {} does not exist. Operation canceled'.format(group))
            return
    for student in students:
        for group in groups:
            try:
                req.post('crowd', 'user/group/direct',
                         params={
                             'username': student.unice_id
                         },
                         json={
                             'name': group
                         })
            except requests.exceptions.HTTPError as e:
                print('Could not add {} to group {}'.format(student.fullname, group))
                reason = {
                    404: 'User {} does not exist'.format(student.fullname),
                    409: 'User {} is already a member of the group {}'.format(student.fullname, group)
                }.get(e.response.status_code, str(e))
                print('Reason: {}'.format(reason))


def delete_students(user_file):
    students = load_students(user_file)
    registered = get_registered_usernames()
    for student in students:
        if student.unice_id not in registered:
            print('The student {} does not exist'.format(student.fullname))
        else:
            try:
                req.delete('crowd', 'user', params={'username': student.unice_id})
                print('The student {} as been deleted'.format(student.fullname))
            except Exception as e:
                print('Could not delete the student {}'.format(student.fullname))
                print('Reason: {}'.format(e))
