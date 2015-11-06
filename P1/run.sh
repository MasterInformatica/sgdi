#! /bin/bash

HADOOP_DIR=/usr/local/hadoop-2.7.1

# Limpiar compilaciones anteriores
rm -rf *.class

# Compilar la clase que contiene el Map y Reduce (opcionalmente Combiner)
javac $1.java -Xlint:unchecked -cp ${HADOOP_DIR}/share/hadoop/common/hadoop-common-2.7.1.jar:${HADOOP_DIR}/share/hadoop/mapreduce/hadoop-mapreduce-client-core-2.7.1.jar:${HADOOP_DIR}/share/hadoop/common/lib/commons-cli-1.2.jar:${HADOOP_DIR}/share/hadoop/mapreduce/lib/hadoop-annotations-2.7.1.jar

# Crear un fichero JAR con todos las clases
jar cf $1.jar *.class

# Borrar el directorio de salida para evitar errores al lanzar la tarea
rm -rf salida/

# Lanzar la tarea MapReduce 
$HADOOP_DIR/bin/hadoop jar $1.jar $1
