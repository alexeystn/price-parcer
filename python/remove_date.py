import pik_lib

db = pik_lib.Database()
print(db.count_records())
db.remove_by_date('2023-05-31')
print(db.count_records())

db.save_changes()
