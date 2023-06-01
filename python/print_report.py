import pik_lib
import json
    
db = pik_lib.Database()

with open('projects.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

s = ''

for days in range(0,7):

    date = db.request("SELECT date('now', '-{0} day')".format(days))[0][0]
    s += date + '\n'

    for project in projects:
        res = db.get_daily_report(project, days)
        s += '{0:16s}'.format(project['name'])
        s += '    '.join(['{0}: {1:3}'.format(r[0], r[1]) for r in res]) + '\n'

    s += '\n'

print(s)

with open('../output/report.txt', 'w') as f:
    f.write(s)
