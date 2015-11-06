import eulexistdb.db

def getCapital(city,id_cap):
    for c in city:
        if(c.attrib["id"]==id_cap):
            return c.find("name").text
    return None





db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q ="""for $e in doc("/db/sgdi/factbook.xml")/mondial/country
return $e"""


r = db.query(q, start =1, how_many=0)


nodes = []

for e in r.results:
    id_cap = e.get("capital")
    nam_cap = getCapital(e.iterchildren(tag="city"),id_cap)
    if(nam_cap is None):
        for c in e.iterchildren(tag="province"):
            nam_cap = getCapital(c.iterchildren(tag="city"),id_cap)
            if not nam_cap is None:
                break;

    nodes+=[(e.attrib["name"],nam_cap)]


print nodes



