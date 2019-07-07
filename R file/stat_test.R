library(xts)
library(quantmod) 
library(PerformanceAnalytics)
library(pracma)
library(fOptions)
library(RND)
library(mnormt)
library(astsa)

setwd("C:/Users/43739/OneDrive/us/2019 spring/paper trading/data")
BPdata<-read.csv(file="intra_bp_2018_1min.csv", header=TRUE, sep=",")
RDSAdata<-read.csv(file="intra_rds-a_2018_1min.csv", header=TRUE, sep=",")
data<-cbind(BPdata,RDSAdata[,-1])
closelist<-data[,c(1,5,9)]
colnames(closelist)<-c("date","BP_close","RDSA_close")

cor(closelist[2],closelist[3])
#0.8544067
#BP=m*RSDA+b
lm_BP_RDSA<-lm(closelist$BP_close~closelist$RDSA_close)
summary(lm_BP_RDSA)
#Intercept
#5.597244
lm_BP_RDSA$coefficients[1]

#Slope
#0.5644122
lm_BP_RDSA$coefficients[2]

res<-closelist$BP_close-(lm_BP_RDSA$coefficients[2]*closelist$RDSA_close+lm_BP_RDSA$coefficients[1])

sd(lm_BP_RDSA$residuals)
#1.355027

mean(lm_BP_RDSA$residuals)
#-2.827601e-15

#AR1
ar1<-sarima(lm_BP_RDSA$residuals,1,0,0)

#Hist
hist(lm_BP_RDSA$residuals,breaks=100,freq = FALSE,main="Histogram of residuals(1min_2018)")
lines(density(lm_BP_RDSA$residuals),col="red")
xseq<-seq(-3*sd(lm_BP_RDSA$residuals)+mean(lm_BP_RDSA$residuals),3*sd(lm_BP_RDSA$residuals)+mean(lm_BP_RDSA$residuals),.01)
densities<-dnorm(xseq,mean(lm_BP_RDSA$residuals),sd(lm_BP_RDSA$residuals))
lines(xseq, densities,col="blue")





#value of the product(done)
avg=0.5
muti=1
plot(lm_BP_RDSA$residuals,type='l',main="value(1min_2018)",ylab="value",ylim=c(-4,4))
upper<-rep(sd(lm_BP_RDSA$residuals)*muti+avg,length(lm_BP_RDSA$residuals))
lower<-rep(-(sd(lm_BP_RDSA$residuals)*muti+avg),length(lm_BP_RDSA$residuals))
mu_upper<-rep(avg,length(lm_BP_RDSA$residuals))
mu_lower<-rep(-avg,length(lm_BP_RDSA$residuals))
limit_loss_upper<-rep(sd(lm_BP_RDSA$residuals)*muti*2+avg,length(lm_BP_RDSA$residuals))
limit_loss_lower<-rep(-(sd(lm_BP_RDSA$residuals)*muti*2+avg),length(lm_BP_RDSA$residuals))
lines(upper,col="red")
lines(lower,col="red")
lines(mu_upper,col="blue")
lines(mu_lower,col="blue")
lines(limit_loss_upper,col="green")
lines(limit_loss_lower,col="green")



#res of res(hist)
res_res<-diff(lm_BP_RDSA$residuals)
res_res<-na.omit(res_res)
hist(res_res,breaks=100,freq = FALSE,main="Histogram of residuals of residuals(1min_2018)",xlim=c(-0.2,0.2),ylim = c(0,65))
lines(density(res_res),col="red")
yseq<-seq(-3*sd(res_res)+mean(res_res),3*sd(res_res)+mean(res_res),.01)
densities<-dnorm(yseq,mean(res_res),sd(res_res))
lines(yseq, densities,col="blue")

mean(res_res)
#8.561096e-06

sd(res_res)
#0.03032336

write.csv(lm_BP_RDSA$residuals, "2018_1min_residuals.csv")

#hist VaR 5%
-quantile(res_res,0.05)*1000*390
#13650

#Delta-Normal VaR
-(-sd(res_res)*1.645+mean(res_res))*1000*390
#19450.61

plot(res_res,type="l",main="change of portfolio value(1min_2018)",ylab="value")
upper_1<-rep(sd(res_res)*3,length(res_res))
lower_1<-rep(-(sd(res_res)*3),length(res_res))
lines(upper_1,col="red")
lines(lower_1,col="red")





#daily value change
data.18BP<-getSymbols("BP",from="2018-01-01",to="2018-12-31",auto.assign = FALSE)
data.18RDSA<-getSymbols("RDS-A",from="2018-01-01",to="2018-12-31",auto.assign = FALSE)
data.close.18BP<-data.18BP[,6]
data.close.18RDSA<-data.18RDSA[,6]
data.18close<-cbind(data.close.18BP,data.close.18RDSA)
colnames(data.18close)<-c("BP","RDSA")
res_res18<-diff(data.18close$BP-(data.18close$RDSA*lm_BP_RDSA$coefficients[2]+lm_BP_RDSA$coefficients[1]))
res_res18<-na.omit(res_res18)


sd(res_res18)
#0.2894637

mean(res_res18)
#0.005978048

plot(res_res18,type="l",main="change of portfolio value(daily_2018)",ylab="value",ylim=c(-2,2))
upper_1_daily<-rep(sd(res_res18)*3+mean(res_res18),length(res_res18))
lower_1_daily<-rep(-(sd(res_res18)*3+mean(res_res18)),length(res_res18))
res_res18<-cbind(res_res18,upper_1_daily,lower_1_daily)
lines(res_res18[,2],col="red")
lines(res_res18[,3],col="red")

#hist
#res of res(hist)(daily)
res_res18<-diff(data.18close$BP-(data.18close$RDSA*lm_BP_RDSA$coefficients[2]+lm_BP_RDSA$coefficients[1]))
res_res18<-na.omit(res_res18)
hist(res_res18,breaks=100,freq = FALSE,main="Histogram of residuals of residuals(daily_2018)",xlim=c(-1,1),ylim = c(0,3))
lines(density(res_res18),col="red")
yseq<-seq(-3*sd(res_res18)+mean(res_res18),3*sd(res_res18)+mean(res_res18),.01)
densities<-dnorm(yseq,mean(res_res18),sd(res_res18))
lines(yseq, densities,col="blue")


########################################################################################2006-2018


data.BP<-getSymbols("BP",from="2006-01-01",to="2018-12-31",auto.assign = FALSE)
data.RDSA<-getSymbols("RDS-A",from="2006-01-01",to="2018-12-31",auto.assign = FALSE)

data.close.BP<-data.BP[,6]
data.close.RDSA<-data.RDSA[,6]
data.close<-cbind(data.close.BP,data.close.RDSA)
colnames(data.close)<-c("BP","RDSA")


plot(data.close)

cor(data.close$BP,data.close$RDSA)
#0.4730847

dailylm<-lm(data.close$BP~data.close$RDSA)
summary(dailylm)

resdaily<-data.close$BP-(dailylm$coefficients[2]*data.close$RDSA+dailylm$coefficients[1])

sd(dailylm$residuals)
#4.447597

mean(dailylm$residuals)
#1.671494e-15

hist(dailylm$residuals,breaks=100,freq = FALSE,main="Histogram of residuals(daily_2006-2018)")
lines(density(dailylm$residuals),col="red")
xseq<-seq(-3*sd(dailylm$residuals)+mean(dailylm$residuals),3*sd(dailylm$residuals)+mean(dailylm$residuals),.01)
densities<-dnorm(xseq,mean(dailylm$residuals),sd(dailylm$residuals))
lines(xseq, densities,col="blue")

plot(resdaily,type='l',main="residuals(daily_2006-2018)")


hist(diff(dailylm$residuals),freq = FALSE)
