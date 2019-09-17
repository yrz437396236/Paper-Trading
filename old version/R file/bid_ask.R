library(xts)
library(quantmod) 
library(pracma)
library(fOptions)
library(RND)
library(mnormt)
library(astsa)
library(ggplot2)
library(aTSA)

#process

setwd("C:/Users/43739/OneDrive/us/2019 spring/paper trading/data/Bloomberg")
BP_bid<-read.csv(file="BP_bid.csv", header=TRUE, sep=",")
BP_ask<-read.csv(file="BP_ask.csv", header=TRUE, sep=",")
RDSA_bid<-read.csv(file="RDSA_bid.csv", header=TRUE, sep=",")
RDSA_ask<-read.csv(file="RDSA_ask.csv", header=TRUE, sep=",")
RDSA_trade<-read.csv(file="RDSA_trade.csv", header=TRUE, sep=",")
BP_trade<-read.csv(file="BP_trade.csv", header=TRUE, sep=",")

rownames(BP_bid)<-as.POSIXlt(BP_bid$Dates,format="%m/%d/%Y %H:%M")
rownames(BP_ask)<-as.POSIXlt(BP_ask$Dates,format="%m/%d/%Y %H:%M")
rownames(RDSA_bid)<-as.POSIXlt(RDSA_bid$Dates,format="%m/%d/%Y %H:%M")
rownames(RDSA_ask)<-as.POSIXlt(RDSA_ask$Dates,format="%m/%d/%Y %H:%M")
rownames(RDSA_trade)<-as.POSIXlt(RDSA_trade$Dates,format="%m/%d/%Y %H:%M")
rownames(BP_trade)<-as.POSIXlt(BP_trade$Dates,format="%m/%d/%Y %H:%M")

BP_bid_ask<-cbind(BP_bid[,1:2],BP_ask[,2][match(rownames(BP_bid), rownames(BP_ask))])
RDSA_bid_ask<-cbind(RDSA_bid[,1:2],RDSA_ask[,2][match(rownames(RDSA_bid), rownames(RDSA_ask))])

BP_bid_ask<-BP_bid_ask[,-1]
RDSA_bid_ask<-RDSA_bid_ask[,-1]

colnames(BP_bid_ask)<-c("BP_bid","BP_ask")
colnames(RDSA_bid_ask)<-c("RDSA_bid","RDSA_ask")

BP_spread_price<-cbind(BP_bid_ask,BP_trade[,2][match(rownames(BP_bid_ask), rownames(BP_trade))])
RDSA_spread_price<-cbind(RDSA_bid_ask,RDSA_trade[,2][match(rownames(RDSA_bid_ask), rownames(RDSA_trade))])

BP_spread_price[2]<-BP_spread_price[2]-BP_spread_price[1]
RDSA_spread_price[2]<-RDSA_spread_price[2]-RDSA_spread_price[1]

BP_spread_price<-na.omit(BP_spread_price[-1])
RDSA_spread_price<-na.omit(RDSA_spread_price[-1])

colnames(BP_spread_price)<-c("spread","price")
colnames(RDSA_spread_price)<-c("spread","price")

BP_spread_return<-BP_spread_price
RDSA_spread_return<-RDSA_spread_price

for (i in 2:length(BP_spread_price[,2]))
{
  BP_spread_return[i,2]=(BP_spread_price[i,2])-(BP_spread_price[i-1,2])
}

for (i in 2:length(RDSA_spread_price[,2]))
{
  RDSA_spread_return[i,2]=(RDSA_spread_price[i,2])-(RDSA_spread_price[i-1,2])
}

BP_spread_return<-BP_spread_return[-1,]
RDSA_spread_return<-RDSA_spread_return[-1,]

colnames(BP_spread_return)<-c("spread","return")
colnames(RDSA_spread_return)<-c("spread","return")
#logreturn is too small for 1min

write.csv(BP_spread_return,"BP_spread_return.csv")
write.csv(RDSA_spread_return,"RSDA_spread_return.csv")

#########################################################

#analysis
#https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test
#https://cran.r-project.org/web/packages/aTSA/aTSA.pdf

#BP
hist(BP_spread_return$spread,breaks=100,freq = FALSE,main="Histogram of BP spread(six month)",xlim=c(-0.1,0.1))
xseq<-seq(-3*sd(BP_spread_return$spread)+mean(BP_spread_return$spread),3*sd(BP_spread_return$spread)+mean(BP_spread_return$spread),.01)
densities<-dnorm(xseq,mean(BP_spread_return$spread),sd(BP_spread_return$spread))
lines(xseq, densities,col="blue")

kurtosis(BP_spread_return$spread)
#2427.319

mean(BP_spread_return$spread)
#0.01038844

sd(BP_spread_return$spread)
#0.01290574

cor(BP_spread_return$spread,sqrt(BP_spread_return$return^2))
#-0.009737485

adf.test(BP_spread_return$spread)
#passed

#########################################################

#RDSA
hist(RDSA_spread_return$spread,breaks=100,freq = FALSE,main="Histogram of RDSA spread(six month)",xlim=c(-0.1,0.1))
xseq2<-seq(-3*sd(RDSA_spread_return$spread)+mean(RDSA_spread_return$spread),3*sd(RDSA_spread_return$spread)+mean(RDSA_spread_return$spread),.01)
densities<-dnorm(xseq2,mean(RDSA_spread_return$spread),sd(RDSA_spread_return$spread))
lines(xseq2, densities,col="blue")

kurtosis(RDSA_spread_return$spread)
#1258.471

mean(RDSA_spread_return$spread)
#0.01104522

sd(RDSA_spread_return$spread)
#0.02846151

cor(RDSA_spread_return$spread,sqrt(RDSA_spread_return$return^2))
#0.02076549

adf.test(BP_spread_return$spread)
#passed

#########################################################




