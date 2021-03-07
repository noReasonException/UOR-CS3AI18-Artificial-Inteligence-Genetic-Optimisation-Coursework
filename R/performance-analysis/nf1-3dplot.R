data=read.csv("hyperF1.csv")
#library("plot3D")
#library("plot3Drgl")
library(car)
attach(data)

head(data)

x <- MR
y <- CR
z <- PS
k <- NORMGENB

scatter3D(
  x, 
  y, 
  z, 
  main = "MR vs CR vs PS vs NF1" ,
  xlab="Mutation Rate",
  ylab="Crossover Rate",
  zlab="Population Size",
  colvar = k, 
  pch = 20,
  theta = 200, 
  phi = 10,
  bty = "b2",
  cex = 2, ticktype = "detailed",
  clab = c("Performance")
  )



plotrgl()

