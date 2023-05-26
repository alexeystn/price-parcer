import json
import pik_lib

# db = pik_database.Database()

with open('projects.json', 'r') as f:
    projects = json.load(f)

for project in projects:
    pairs = pik_lib.download_flats(project, archive_enabled=True)
    print(len(pairs))
    # download_id_price_pairs(project, archive_enabled=True)
    #for price, flat_id in pairs:
    #    db.write(project['url'], price, flat_id)

# db.save_changes()
