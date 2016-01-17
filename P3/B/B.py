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
    db.usuarios.insert_one(user)



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

    db.usuarios.update_one({"alias": alias}, {"$set":user})



# 3. Añadir una pregunta
def add_question():
    pass


# 4. Añadir una respuesta a una pregunta.
def add_answer():
    pass


# 5. Comentar una respuesta.
def add_comment():
    pass


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
def get_question():
    pass


# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def get_question_by_tag():
    pass


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
            "fecha_creacion": fecha
    }



if __name__ == '__main__' : 

    # Conexión con la base de datos
    client = MongoClient('localhost',27017)
    db = client['sgdi_grupo04']

    #insert_user("alias", "n", "a", "v", "n", "c", "p", ["asd", "bl"])
    #update_user("alias", "a", "a", "a", "a", "a", "a", [])


    print get_user("ShW")
    print "----------------------------------------------------------------------"
    print get_uses_by_expertise("SQL")

