from python.util import pw_gen


class User:
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    @property
    def username(self):
        return '{}_{}'.format(self.firstname[:3], self.lastname[:3]).upper()

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    @property
    def display_name(self):
        return self.fullname

    def get_crowd_format(self, pw_default=None):
        if pw_default is None:
            pw_default = pw_gen(10)
        crowd_format = {
            'name': self.username,
            'first-name': self.firstname,
            'last-name': self.lastname,
            'display-name': self.display_name,
            'email': self.email,
            'password': {
                'value': pw_default
            },
            'active': True
        }
        return crowd_format


class Student(User):
    def __init__(self, row):
        super(Student, self).__init__(row[1], row[0], row[3])
        self.year = None
        self.unice_id = row[2]
        self.mystery_field = None
        self.ine = row[7]

    @property
    def username(self):
        return self.unice_id
