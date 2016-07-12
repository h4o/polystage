import Groups
import Users

# Groups.delete(['4a-2015'])
# Users.remove_students('students.csv')
Users.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)


