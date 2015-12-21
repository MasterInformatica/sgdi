#!/bin/bash


SRC=$1

xelatex -shell-escape $SRC
xelatex -shell-escape $SRC


FICH="${1%.*}"
echo $FICH

#Borramos lo que genera y no queremos
rm $FICH.aux $FICH.log $FICH.nav $FICH.out $FICH.snm $FICH.toc $FICH.vrb texput.log
