# -*- coding: utf-8 -*-
"""
Autores: Luis M. Costero Valero & Jesús Doménech Arellano
Grupo 04

Este código es fruto ÚNICAMENTE del trabajo de sus miembros. Declaramos no 
haber colaborado de ninguna manera con otros grupos, haber compartido el ćodigo 
con otros ni haberlo obtenido de una fuente externa.
"""
import pymongo
from pymongo import MongoClient
from datetime import datetime
from bson import json_util
from bson import ObjectId
import json
from B import *

def todas():
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg1()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg2()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg3()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg4()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg5()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg6()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg7()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg8()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg9()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg10()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg11()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg12()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg13()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg14()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg15()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"
    preg16()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>"

# 1. Añadir un usuario
def preg1():
    print "Pregunta 1: Añadir un usuario"
    print insert_user("ShW7", "Sherlock", "Holmes", 
                      "Baker Street", "221B", "London", "England", 
                      ["SQL", "Tor", "recovering"])
    print "¿Y si ya existe?"
    print insert_user("ShW7", "Sherlock", "Holmes", 
                      "Baker Street", "221B", "London", "England", 
                      ["SQL", "Tor", "recovering"])

# 2. Actualizar un usuario
def preg2():
    print "Pregunta 2: Actualizar un usuario"
    print update_user("alias", "a", "a", "a", "a", "a", "a", [])
    print "¿Y si NO existe?"
    print update_user("1alias", "a", "a", "a", "a", "a", "a", [])

# 3. Añadir una pregunta
def preg3():
    print "Pregunta 3: Añadir una pregunta"
    print add_question("Titulo sobre SQL", "ShW", "Como puedo realizar un join por la izquierda?", ["sql", "bbdd"])
    print "¿Y si NO existe el usuario?"
    print add_question("Titulo sobre SQL", "NuncaExistire", "Como puedo realizar un join por la izquierda?", ["sql", "bbdd"])

# 4. Añadir una respuesta a una pregunta
def preg4():
    print "Pregunta 4: Añadir una respuesta a una pregunta"
    print add_answer(ObjectId("569d3a341204b70e9ce41037"), "ShW", 
                     "la clave es imaginar un objeto como un diccionario de punteros a función")
    print "¿Y si no existe la pregunta?"
    print add_answer(ObjectId("569d3a341204b00e9ce41037"), "ShW", "Respo")

    print "¿Y si no existe el usuario que responde?"
    print add_answer(ObjectId("569d3a341204b00e9ce41037"), "NoExisto", "Respo")

# 5. Comentar una respuesta.
def preg5():
    print "Pregunta 5: Comentar una respuesta"
    print add_comment(ObjectId("569d3f9e1204b712cd7d58d8"), "Poison",
                      "Esto es un comentario a tu respuesta. Muy buena!")
    print "¿Y si no existe la respuesta?"
    print add_comment(ObjectId("569d3a321204b00e9ce41037"), "ShW", "Respo")

    print "¿Y si no existe el usuario que comenta?"
    print add_comment(ObjectId("569d3a341204b00e9ce41037"), "NoExisto", "Respo")


# 6. Puntuar una respuesta.
def preg6():
    print "Pregunta 6: Puntuar una respuesta"
    print score_answer(ObjectId("569d3f9e1204b712cd7d58d7"), -1, "alias")
    print "¿Y si no existe la respuesta?"
    print score_answer(ObjectId("369d3f9e1204b712cd7d58d7"), -1, "alias")
    print "¿Y si no existe el usuario que puntúa?"
    print score_answer(ObjectId("569d3f9e1204b712cd7d58d7"), -1, "NoExisto")

# 7. Modificar una puntuacion de buena a mala o viceversa.
def preg7():
    print "Pregunta 7: Modificar una puntuacion de buena a mala o viceversa"
    print update_score(ObjectId("569e20e11204b70e4eb8bf09"))
    print "¿Y si no existe la puntuación?"
    print update_score(ObjectId("369e20e11204b70e4eb8bf09"))

# 8. Borrar una pregunta junto con todas sus respuestas, comentarios y 
# puntuaciones
def preg8():
    print "Pregunta 8. Borrar una pregunta junto con todas sus respuestas, comentarios y puntuaciones"
    print delete_question(ObjectId("569d3a341204b70e9ce41036"))
    print "¿Y si la pregunta no existe?"
    print delete_question(ObjectId("569d3a341204b70e9ce41036"))

# 9. Visualizar una determinada pregunta junto con todas sus contestaciones
# y comentarios. A su vez las contestaciones vendran acompañadas de su
# numero de puntuaciones buenas y malas.
def preg9():
    print "Pregunta 9: Visualizar una determinada pregunta junto con todas sus contestaciones y comentarios. A su vez las contestaciones vendran acompañadas de su numero de puntuaciones buenas y malas"
    print get_question(ObjectId("569d3a341204b70e9ce41037"))
    print "¿Y si no existe la pregunta?"
    print get_question(ObjectId("369d3a341204b70e9ce41037"))

# 10. Buscar preguntas con unos determinados tags y mostrar su titulo, su autor
# y su numero de contestaciones.
def preg10():
    print "Pregunta 10: Buscar preguntas con unos determinados tags y mostrar su titulo, su autor y su numero de contestaciones"
    print get_question_by_tag(["sql"])
    print "¿Y con dos tags?"
    print get_question_by_tag(["sql","bbdd"])
    print "¿Y si no hay nada con ese tag?"
    print get_question_by_tag(["nohay"])

# 11. Ver todas las preguntas o respuestas generadas por un determinado usuario.
def preg11():
    print "Pregunta 11: Ver todas las preguntas o respuestas generadas por un determinado usuario"
    print get_entries_by_user("ShW")
    print "¿Y si el usuario no existe?"
    print get_entries_by_user("Noexiste")


# 12. Ver todas las puntuaciones de un determinado usuario ordenadas por 
# fecha. Este listado debe contener el tıtulo de la pregunta original 
# cuya respuesta se puntuo.
def preg12():
    print "Pregunta 12: Ver todas las puntuaciones de un determinado usuario ordenadas por fecha. Este listado debe contener el tıtulo de la pregunta original cuya respuesta se puntuo"
    print get_scores("ShW")
    print "¿Y si el usuario no existe?"
    print get_scores("Noexiste")

# 13. Ver todos los datos de un usuario.
def preg13():
    print "Pregunta 13: Ver todos los datos de un usuario"
    print get_user("ShW")
    print "¿Y si el usuario no existe?"
    print get_user("Noexiste")

# 14. Obtener los alias de los usuarios expertos en un determinado tema.
def preg14():
    print "Pregunta 14: Obtener los alias de los usuarios expertos en un determinado tema" 
    print get_uses_by_expertise("SQL")
    print "¿Y si el tema no existe?"
    print get_uses_by_expertise("sql")
    

# 15. Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo
# el numero de contestaciones recibidas.
def preg15():
    print "Pregunta 15: Visualizar las n preguntas mas actuales ordenadas por fecha, incluyendo el numero de contestaciones recibidas"
    print get_newest_questions(2)
    print "¿Y si pedimos más de las que hay?"
    print get_newest_questions(100)

# 16. Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por
# numero de contestaciones recibidas.
def preg16():
    print "Pregunta 16: Ver n preguntas sobre un determinado tema, ordenadas de mayor a menor por numero de contestaciones recibidas"
    print get_questions_by_tag(2, ["sql"])
