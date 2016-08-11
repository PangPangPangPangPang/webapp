#!/usr/bin/env python

import os, json, sys

token = '1ZakwQXvhth3MNvRbTjA'
home_path = os.path.expandvars('$HOME')
project_name = 'SinaNews'

if len(sys.argv) != 2:
    print '---------------------------------------------'
    print 'Confirm to change your own token from gitlab!'
    print '---------------------------------------------'
else:
    token = sys.argv[1]

output = os.popen('curl -L http://10.210.97.101:80/api/v3/projects?private_token=' + token)

group = json.loads(output.read())

for item in group:
    name = item.get('name')
    address = item.get('ssh_url_to_repo')
    if name == project_name:
        exist = False
        os.chdir(home_path)
        paths = os.listdir('./')
        for path in paths:
            if name == path.decode('utf8'):
                exist = True
        if exist == True:
            os.system('rm -rf ' + "./" + name)
        os.system('git clone ' + address + ' ' + name)

        # change to work branch
        os.chdir('./' + name)
        os.system('git checkout develop')