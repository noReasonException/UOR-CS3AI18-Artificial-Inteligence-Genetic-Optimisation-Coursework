dataF1=read.csv("perfF1.csv")
dataF2=read.csv("perfF4.csv")
library(car)


head(data)

x1 <- dataF1$R1[1:100]
y1 <- dataF1$FIT1[1:100]
x2 <- dataF2$R2[1:100]
y2 <- dataF2$FIT2[1:100]


plot(x1, y1, main="F1 and F4 performance with MR=0.2,CR=0.8,PO=100, Uniform mutation and Elitistic select enabled\n10 simulations average",
     xlab="Generations", ylab="Fitness ", pch=19,type="l",col="#FF5728")  
lines(x2, y2, col="#00B0BA", lwd=2)
legend(80,60,c("F1","F4"), lwd=c(5,5), col=c("#00B0BA","#FF5728"), y.intersp=1.5)


