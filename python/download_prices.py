import json
import sys
import pik_lib

if len(sys.argv) > 1:
    if 'w' in sys.argv[1]:
        write_enabled = True
else:
    write_enabled = False

archive_enabled = True


db = pik_lib.Database()
projects = pik_lib.load_project_list()

for project in projects:

    print('{0}... '.format(project['name']), end='', flush=True)
    flats = pik_lib.download_flats(project, archive_enabled)
    print(len(flats))
    
    for flat in flats:
        db.write(flat)


if write_enabled:
    db.save_changes()
