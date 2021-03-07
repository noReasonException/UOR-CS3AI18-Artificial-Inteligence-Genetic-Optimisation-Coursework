dataF1=read.csv("perfF1.csv")
dataF2=read.csv("perfF4.csv")
library(car)


head(data)

x1 <- dataF1$R1[1:80]
y1 <- dataF1$FIT1[1:80]
x2 <- dataF2$R2[1:80]
y2 <- dataF2$FIT2[1:80]


plot(x1, y1, main="3, 10 round averages for F1(MR=0.2,CR=0.8,PO=1000), Generations on range [0,30]",
     xlab="Generations", ylab="F1(x) ", pch=19,type="l",col="#FF5728")  
lines(x2, y2, col="#00B0BA", lwd=2)
legend(70,60,c("R1","R2"), lwd=c(2,2), col=c("#E7C582","#00B0BA"), y.intersp=1.5)


