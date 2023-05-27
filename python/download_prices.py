import json
import pik_lib

# db = pik_database.Database()

projects = pik_lib.load_project_list()

for project in projects:

    print('{0}... '.format(project['name']), end='')
    flats = pik_lib.download_flats(project, archive_enabled=True)
    print(len(flats))
    
    # download_id_price_pairs(project, archive_enabled=True)
    # for price, flat_id in pairs:
    #     db.write(project['url'], price, flat_id)

# db.save_changes()
