
x1 <- seq(-2, 2, length=1000)
y1 <- dnorm(x1, mean=0, sd=1)
plot(x1, y1, type="l", lwd=1,xlim=c(-2, 2), ylim=c(0, 0.6),main="Gene mutation distribution: Uniform vs Gaussian(0,1)")
x2 <- seq(-2, 2, length=1000)
y2 <- dunif(x2,-1,1)
lines(x2, y2, col="#00B0BA", lwd=3)