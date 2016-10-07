#!/bin/bash

BD="sgdi_grupo04"

# borramos todo
mongo $BD --eval "db.dropDatabase();"

# cargamos la BD
mongoimport -d $BD -c preguntas --file preguntas.json
mongoimport -d $BD -c respuestas --file respuestas.json
mongoimport -d $BD -c usuarios --file usuarios.json
mongoimport -d $BD -c votos --file votos.json


# creamos los indices necesarios
mongo $BD --eval "db.usuarios.ensureIndex({alias:1},{unique:true});"
mongo $BD --eval "db.preguntas.ensureIndex({alias:1});"
mongo $BD --eval "db.respuestas.ensureIndex({alias:1});"
mongo $BD --eval "db.votos.ensureIndex({alias:1});"
