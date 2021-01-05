from database import Database

db = Database()
db2 = Database()
data = db.get_all()
data = db2.get_all()
data = db.get_all()
data = db2.get('name-1')
data = db.get_all()
data = db2.get_all()
data = db.get_all()
data = db2.get_all()
data = db.get_all()
print(data)
