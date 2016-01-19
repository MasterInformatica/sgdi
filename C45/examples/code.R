hyp <- read.table(file="./hypo.data",header=FALSE,sep=",")
hyp <- hyp[ sample( nrow( hyp ) ), ]
attr <- hyp[,2:26] 
clas <- hyp[,1] 
trainAttr <- attr[1:3000,] 
trainClas <- clas[1:3000] 
testAttr <- attr[3001:3163,] 
testClas <- clas[3001:3163] 
library(C50) 
model <- C50::C5.0( trainAttr, trainClas ) 
p <- predict( model, testAttr, type="class" )
acierto <- sum( p == testClas ) / length( p )


