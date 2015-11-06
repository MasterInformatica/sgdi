import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

q ="""for $e in doc("/db/sgdi/factbook.xml")/mondial/country
      let $t := $e/name
      where count($e/encompassed) > 1  
19"      return $t"""
for $t in doc("/db/sgdi/factbook.xml")/mondial
    let $s:=$t/continent[@name="America"]
    let $country:= $t/country
    where $t/country/encompassed/@continent = data($s/@id)
    and  $t/country/@total_area > 100000

    return $country

r = db.query(q, start =1, how_many=0)


nodes = []

for e in r.results:
    nodes+=[e.text]


print nodes



