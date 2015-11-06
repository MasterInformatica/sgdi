import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q ="""for $e in doc("/db/sgdi/factbook.xml")/mondial/country
return $e"""


r = db.query(q, start =1, how_many=0)


nodes = []

for e in r.results:
    nodes += [(e.get("name"),e.get("id"),e.get("datacode"))]


print nodes



