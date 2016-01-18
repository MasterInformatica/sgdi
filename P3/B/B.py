# -*- coding: utf-8 -*-
"""
Autores: Luis M. Costero Valero & Jesús Doménech Arellano
Grupo 04

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
"""

from pymongo import MongoClient
from datetime import datetime
from bson import json_util
from bson import ObjectId
import json

#################################################################
## Es necesario añadir los parámetros adecuados a cada función ##
#################################################################


#TODO: Pasar todo a txt. Hay que deolver json

# 1. Añadir un usuario
def insert_user(alias, nombre, apellidos, calle, numero, ciudad, pais,
                experiencia ):

    user = createUser(alias, nombre, apellidos, calle, numero, ciudad, pais, experiencia) 
    ret = db.usuarios.insert_one(user)

    return json_util.dumps({"inserted_id":ret.inserted_id})


# 2. Actualizar un usuario
def update_user(alias, nombre, apellidos, calle, numero, ciudad, pais,
                experiencia, fecha=None):

    """ La versión de pymongo que estamos utilizando no permite actualizar por defecto
    todos los campos de manera directa, sino que obliga a utilizar al menos algún operador
    de actualización ($set en este caso):
        raise ValueError('update only works with $ operators')
    """
    user = createUser(alias, nombre, apellidos, calle, numero, ciudad,
                      pais, experiencia, fecha)

    ret = db.usuarios.update_one({"alias": alias}, {"$set":user})

    return json_util.dumps({"modified_count": ret.modified_count})



# 3. Añadir una pregunta
def add_question(titulo, alias, texto, tags, fecha=None):
    """ Suponemos que la API ha realizado las comprobaciones de seguridad pertinentes,
    y el alias del usuario existe """

    # 1.- Insertamos la pregunta y guardamos su id
    question = createQuestion(titulo, alias, texto, tags, fecha)
    id = db.preguntas.insert_one(question).inserted_id

    # 2.- Guaramos en la tabla de usuarios la referencia
    db.usuarios.update_one({"alias":alias},
                           {"$push": { "preguntas": id } })

    
    return json_util.dumps({"inserted_id": id})



# 4. Añadir una respuesta a una pregunta.
def add_answer(pregunta_id, alias, texto, fecha=None):
    #1.- Insertamos la respuesta y guardamos su id
    answer = createAnswer(pregunta_id, alias, texto, fecha)
    id = db.respuestas.insert_one(answer).inserted_id
    
    #2.- Guardamos la referencia tanto en las preguntas como en el usuario
    db.usuarios.update_one({"alias": alias},
                           {"$push": {"respuestas": id} })
    db.preguntas.update_one({"_id": pregunta_id},
                            {"$push" : {"respuestas": id} })

    return json_util.dumps({"inserted_id": id})
    


# 5. Comentar una respuesta.
def add_comment(respuesta_id, alias, texto, fecha=None):
    comment = createComment(alias, texto, fecha=None)

    id = db.respuestas.update_one({"_id":respuesta_id},
                                  {"$push": { "comentarios" : comment}})

    return json_util.dumps({"modified_count": id.modified_count})


# 6. Puntuar una respuesta.
def score_answer():
    pass


# 7. Modificar una puntuacion de buena a mala o viceversa.
def update_score():
    pass


# 8. Borrar una pregunta junto con todas sus respuestas, comentarios y 
# puntuaciones
def delete_question():
    pass


# 9. Visualizar una determinada pregunta junto con todas sus contestaciones
# y comentarios. A su vez las contestaciones vendran acompañadas de su
# numero de puntuaciones buenas y malas.
def get_question(pregunta_id):
    #1.- Conseguir la pregunta
    question = db.preguntas.find_one({"_id": pregunta_id})

    #2.- Conseguir todos las contestaciones y comentarios
    answers = db.respuestas.find({"_id": { "$in": question["respuestas"]}},
                                 {"pregunta_id": 0 })
    
    return json_util.dumps({"question" : question,
                            "answers" : answers})


# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def get_question_by_tag(tags):

    if not isinstance(tags, list):
        tags = [tags]


    #Para realizar la consulta y quedarnos solamente con los campos que queremos,
    #y además contar el número de elementos, realizamos un aggregation pipeline

    pipeline = [
        {"$match": {"tags": {"$all": tags}}},
        {"$project": {
            "alias": 1,
            "titulo": 1,
            "_id": 0,
            "num_contestaciones": { "$size": "$respuestas"}
           }
         }
    ]
         
    questions = db.preguntas.aggregate(pipeline)

    return json_util.dumps(questions)


# 11. Ver todas las preguntas o respuestas generadas por un determinado usuario.
def get_entries_by_user():
    pass


# 12. Ver todas las puntuaciones de un determinado usuario ordenadas por 
# fecha. Este listado debe contener el tıtulo de la pregunta original 
# cuya respuesta se puntuo.
def get_scores():
    pass


# 13. Ver todos los datos de un usuario.
def get_user(alias):
    #TODO: cambiar de acuerdo al diseño final de la bd
    filtro = {"_id": 0,
              "preguntas": 0,
              "respuestas": 0
          }
    user = db.usuarios.find_one({"alias":alias}, filtro)
    
    return json_util.dumps(user)



# 14. Obtener los alias de los usuarios expertos en un determinado tema.
def get_uses_by_expertise(topic):
    
    alias = db.usuarios.find({"experiencia":topic},  {"alias": 1, "_id": 0})
    return json_util.dumps(alias)


# 15. Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo
# el numero de contestaciones recibidas.
def get_newest_questions():
    pass


# 16. Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por
# numero de contestaciones recibidas.
def get_questions_by_tag():
    pass
    
    



################################################################################
############################  FUNCIONES AUXILIARES  ############################
################################################################################


#Dados los campos de una direccion, devuelve el objeto para insertar
def createDirection(calle, numero, ciudad, pais):
    return {"calle": calle,
            "numero": numero,
            "ciudad": ciudad,
            "pais": pais}

#Crea un usuario para insertar en la bd. si la fecha en nula, pone la actual
def createUser(alias, nombre, apellidos, calle, numero, ciudad, pais,
               experiencia, fecha=None):
    dir = createDirection(calle, numero, ciudad, pais)

    if not isinstance(experiencia, list):
        experiencia = [experiencia]

    if fecha is None:
        fecha = datetime.utcnow()

    return {"alias": alias,
            "nombre": nombre,
            "apellidos": apellidos,
            "direccion": dir,
            "experiencia": experiencia,
            "fecha_creacion": fecha,
            "preguntas": [],
            "respuestas": []
    }


#Crea una pregunta a partir de su contenido dado por parámetro
def createQuestion( titulo, alias, texto, tags, fecha=None):
    if not isinstance(tags, list):
        tags = [tags]
    if fecha is None:
        fecha = datetime.utcnow()

    return {"titulo": titulo,
            "alias": alias,
            "texto": texto,
            "tags" : tags,
            "fecha_creacion": fecha,
            "respuestas" : []
        }


#Dados los datos de una respuesta, crea el objeto a insertar en la bd
def createAnswer(pregunta_id, alias, texto, votos_pos=0, votos_neg=0, fecha=None):
    if fecha is None:
        fecha = datetime.utcnow()

    return {"pregunta_id" : pregunta_id,
            "alias" : alias,
            "texto" : texto,
            "votos_pos" : votos_pos,
            "votos_neg" : votos_neg,
            "fecha_creacion" : fecha,
            "comentarios" : []
        }


#Dados los datos de un comentario, crea el objeto para insertar en la bd
def createComment(alias, texto, fecha=None) :
    if fecha is None:
        fecha = datetime.utcnow()

    return {"alias": alias,
            "texto": texto,
            "fecha_creacion": fecha
            }
    

if __name__ == '__main__' : 

    # Conexión con la base de datos
    client = MongoClient('localhost',27017)
    db = client['sgdi_grupo04']


    # usuarios
    #print insert_user("ShW", "Sherlock", "Holmes", "Baker Street", "221B", "London", "England", ["SQL", "Tor", "recovering"])
    #print insert_user("Poison", "Hercules", "Poirot", "Le grand place", "3", "Bruxeles", "Belgium", ["Poison", "SQL", "murders"])
    #print insert_user("alias", "n", "a", "v", "n", "c", "p", ["asd", "bl"])
    #print update_user("alias", "a", "a", "a", "a", "a", "a", [])
    #print get_user("ShW")
    #print get_uses_by_expertise("SQL")

    #preguntas
    #print add_question("Mejor manera de envenenar?", "Poison", "Me han encargado un trabajo, y necesito saber los dístintos métodos que existen para envenenar a una persona actualmente.", ["poison", "crimen"])
    #print add_question("tit", "ShW", "asd", ["poison", "sql"])
    #print get_question_by_tag(["poison", "sql"])

    #respuestas
    #print add_answer(ObjectId("569ccdfcb2c6de091937d0ba"), "ShW", "reskj puesta")

    print get_question(ObjectId("569ccdfcb2c6de091937d0ba"))
    #print add_comment(ObjectId("569cd3ceb2c6de0ac2895e91"), "Perico", "esto es un comentario")
