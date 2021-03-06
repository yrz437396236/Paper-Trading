library(xts)
library(quantmod) 
library(PerformanceAnalytics)
library(pracma)
library(moments)
library(RND)
library(mnormt)
library(astsa)
library(aTSA)

#read data
setwd("C:/Users/43739/OneDrive/us/2019 spring/paper trading/data/yahoo finance")
BP2007<-read.csv(file="BP/BP_2007.csv", header=TRUE, sep=",")
BP2008<-read.csv(file="BP/BP_2008.csv", header=TRUE, sep=",")
BP2009<-read.csv(file="BP/BP_2009.csv", header=TRUE, sep=",")
BP2010<-read.csv(file="BP/BP_2010.csv", header=TRUE, sep=",")
BP2011<-read.csv(file="BP/BP_2011.csv", header=TRUE, sep=",")
BP2012<-read.csv(file="BP/BP_2012.csv", header=TRUE, sep=",")
BP2013<-read.csv(file="BP/BP_2013.csv", header=TRUE, sep=",")
BP2014<-read.csv(file="BP/BP_2014.csv", header=TRUE, sep=",")
BP2015<-read.csv(file="BP/BP_2015.csv", header=TRUE, sep=",")
BP2016<-read.csv(file="BP/BP_2016.csv", header=TRUE, sep=",")

RDS_A2007<-read.csv(file="RDS-A/RDS-A_2007.csv", header=TRUE, sep=",")
RDS_A2008<-read.csv(file="RDS-A/RDS-A_2008.csv", header=TRUE, sep=",")
RDS_A2009<-read.csv(file="RDS-A/RDS-A_2009.csv", header=TRUE, sep=",")
RDS_A2010<-read.csv(file="RDS-A/RDS-A_2010.csv", header=TRUE, sep=",")
RDS_A2011<-read.csv(file="RDS-A/RDS-A_2011.csv", header=TRUE, sep=",")
RDS_A2012<-read.csv(file="RDS-A/RDS-A_2012.csv", header=TRUE, sep=",")
RDS_A2013<-read.csv(file="RDS-A/RDS-A_2013.csv", header=TRUE, sep=",")
RDS_A2014<-read.csv(file="RDS-A/RDS-A_2014.csv", header=TRUE, sep=",")
RDS_A2015<-read.csv(file="RDS-A/RDS-A_2015.csv", header=TRUE, sep=",")
RDS_A2016<-read.csv(file="RDS-A/RDS-A_2016.csv", header=TRUE, sep=",")

BP2007<-na.omit(BP2007)
BP2008<-na.omit(BP2008)
BP2009<-na.omit(BP2009)
BP2010<-na.omit(BP2010)
BP2011<-na.omit(BP2011)
BP2012<-na.omit(BP2012)
BP2013<-na.omit(BP2013)
BP2014<-na.omit(BP2014)
BP2015<-na.omit(BP2015)
BP2016<-na.omit(BP2016)

RDS_A2007<-na.omit(RDS_A2007)
RDS_A2008<-na.omit(RDS_A2008)
RDS_A2009<-na.omit(RDS_A2009)
RDS_A2010<-na.omit(RDS_A2010)
RDS_A2011<-na.omit(RDS_A2011)
RDS_A2012<-na.omit(RDS_A2012)
RDS_A2013<-na.omit(RDS_A2013)
RDS_A2014<-na.omit(RDS_A2014)
RDS_A2015<-na.omit(RDS_A2015)
RDS_A2016<-na.omit(RDS_A2016)
#due to data miss in 2017, our test end in 2016
########################################################################################

lmresult <- data.frame("year"=numeric(),"slope"=numeric(),"intercept"=numeric(),"mean_res"=numeric(),"sd_res"=numeric(),"kurtosis_res"=numeric()) 
lm2008<-lm(BP2007$close~RDS_A2007$close)
row2008<- c(2008,lm2008$coefficients[2],lm2008$coefficients[1],mean(lm2008$residuals),sd(lm2008$residuals),kurtosis(lm2008$residuals))
lmresult<-rbind(lmresult,row2008)

lm2009<-lm(BP2008$close~RDS_A2008$close)
row2009<- c(2009,lm2009$coefficients[2],lm2009$coefficients[1],mean(lm2009$residuals),sd(lm2009$residuals),kurtosis(lm2009$residuals))
lmresult<-rbind(lmresult,row2009)

lm2010<-lm(BP2009$close~RDS_A2009$close)
row2010<- c(2010,lm2010$coefficients[2],lm2010$coefficients[1],mean(lm2010$residuals),sd(lm2010$residuals),kurtosis(lm2010$residuals))
lmresult<-rbind(lmresult,row2010)

lm2011<-lm(BP2010$close~RDS_A2010$close)
row2011<- c(2011,lm2011$coefficients[2],lm2011$coefficients[1],mean(lm2011$residuals),sd(lm2011$residuals),kurtosis(lm2011$residuals))
lmresult<-rbind(lmresult,row2011)

lm2012<-lm(BP2011$close~RDS_A2011$close)
row2012<- c(2012,lm2012$coefficients[2],lm2012$coefficients[1],mean(lm2012$residuals),sd(lm2012$residuals),kurtosis(lm2012$residuals))
lmresult<-rbind(lmresult,row2012)

lm2013<-lm(BP2012$close~RDS_A2012$close)
row2013<- c(2013,lm2013$coefficients[2],lm2013$coefficients[1],mean(lm2013$residuals),sd(lm2013$residuals),kurtosis(lm2013$residuals))
lmresult<-rbind(lmresult,row2013)

lm2014<-lm(BP2013$close~RDS_A2013$close)
row2014<- c(2014,lm2014$coefficients[2],lm2014$coefficients[1],mean(lm2014$residuals),sd(lm2014$residuals),kurtosis(lm2014$residuals))
lmresult<-rbind(lmresult,row2014)

lm2015<-lm(BP2014$close~RDS_A2014$close)
row2015<- c(2015,lm2015$coefficients[2],lm2015$coefficients[1],mean(lm2015$residuals),sd(lm2015$residuals),kurtosis(lm2015$residuals))
lmresult<-rbind(lmresult,row2015)

lm2016<-lm(BP2015$close~RDS_A2015$close)
row2016<- c(2016,lm2016$coefficients[2],lm2016$coefficients[1],mean(lm2016$residuals),sd(lm2016$residuals),kurtosis(lm2016$residuals))
lmresult<-rbind(lmresult,row2016)

lm2017<-lm(BP2016$close~RDS_A2016$close)
row2017<- c(2017,lm2017$coefficients[2],lm2017$coefficients[1],mean(lm2017$residuals),sd(lm2017$residuals),kurtosis(lm2017$residuals))
lmresult<-rbind(lmresult,row2017)

colnames(lmresult)<-c("year","slope","intercept","mean_res","sd_res","kurtosis_res")
write.csv(lmresult, file = "lmresult.csv", row.names = FALSE)
########################################################################################end
hist(lm2008$residuals)
hist(lm2008$residuals,breaks=100,freq = FALSE,main="Histogram of residuals(daily_2008)")
lines(density(lm2008$residuals),col="red")
xseq<-seq(-3*sd(lm2008$residuals)+mean(lm2008$residuals),3*sd(lm2008$residuals)+mean(lm2008$residuals),.01)
densities<-dnorm(xseq,mean(lm2008$residuals),sd(lm2008$residuals))
lines(xseq, densities,col="blue")


kurtosis(na.omit(diff(lm2008$residuals)))
