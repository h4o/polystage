from Requester import req


def create():
    a = {
        'name': 'IslandPerm',
        'description': 'Yolo',
        'permissions': [
            {
                'holder': {
                    'type': 'group',
                    # 'type': 'projectRole',
                    'parameter': 'jira-administrator',
                    'expand': 'projectRole'
                },
                'permission': 'ADMINISTER_PROJECTS'
            }
        ]
    }
    b = {
        'name': 'skdlqkskdlqskd'
    }
    c = {
        'name': 'mpolk',
        'permissions': [
            {
                'holder': {
                    'type': 'projectRole',
                    'parameter': 'developers'
                },
                'permission': 'ADMINISTER_PROJECTS'
            }
        ]
    }

    # req.post('jira', 'permissionscheme', json=b)
    req.post('jira', 'permissionscheme', json=b)
    # req.post('jira', 'permissionscheme', json=a, params={'expand': 'projectRole'})


create()
