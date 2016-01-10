#!/bin/bash


SRC=$1
FICH="${1%.*}"

pdflatex -shell-escape $SRC
bibtex $FICH
pdflatex -shell-escape $FICH


echo $FICH

#Borramos lo que genera y no queremos
rm $FICH.aux $FICH.log $FICH.nav $FICH.out $FICH.snm $FICH.toc $FICH.vrb texput.log
