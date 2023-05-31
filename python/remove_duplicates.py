import json
import pik_lib


db = pik_lib.Database()
print(db.count_records())

res = db.get_duplicates()

for r in res:
    db.remove_by_id(r[0])

print(db.count_records())

print(len(res))
print(set([r[2] for r in res]))

db.save_changes()
