#!/bin/bash

BD="sgdi_grupo04"

#borramos todo
mongo $BD --eval "db.dropDatabase();"

mongoimport -d $BD -c preguntas --file preguntas.json
mongoimport -d $BD -c respuestas --file respuestas.json
mongoimport -d $BD -c usuarios --file usuarios.json
mongoimport -d $BD -c votos --file votos.json
