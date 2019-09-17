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
RDSA_trade<-read.csv(file="RDSA_trade.csv", header=TRUE, sep=",")
BP_trade<-read.csv(file="BP_trade.csv", header=TRUE, sep=",")

rownames(BP_trade)<-as.POSIXlt(BP_trade$Dates,format="%m/%d/%Y %H:%M")
rownames(RDSA_trade)<-as.POSIXlt(RDSA_trade$Dates,format="%m/%d/%Y %H:%M")

BP_volume_price<-cbind(BP_trade[,-1],BP_trade[,2])
RDSA_volume_price<-cbind(RDSA_trade[,-1],RDSA_trade[,2])

BP_volume_price<-BP_volume_price[,-1]
RDSA_volume_price<-RDSA_volume_price[,-1]

colnames(BP_volume_price)<-c("volume","price")
colnames(RDSA_volume_price)<-c("volume","price")

BP_volume_return<-BP_volume_price
RDSA_volume_return<-RDSA_volume_price

for (i in 2:length(BP_volume_price[,2]))
{
  BP_volume_return[i,2]=(BP_volume_price[i,2])-(BP_volume_price[i-1,2])
}

for (i in 2:length(RDSA_volume_price[,2]))
{
  RDSA_volume_return[i,2]=(RDSA_volume_price[i,2])-(RDSA_volume_price[i-1,2])
}

BP_volume_return<-BP_volume_return[-1,]
RDSA_volume_return<-RDSA_volume_return[-1,]

colnames(BP_volume_price)<-c("volume","return")
colnames(RDSA_volume_price)<-c("volume","return")

write.csv(BP_volume_return,"BP_volume_return.csv")
write.csv(RDSA_volume_return,"RSDA_volume_return.csv")

#########################################################

#analysis

#BP
kurtosis(BP_volume_return$volume)
#82.37227

mean(BP_volume_return$volume)
#14134.39

sd(BP_volume_return$volume)
#18150.24

cor(BP_volume_return$volume,sqrt(BP_volume_return$return^2))
#0.3196601
# need to notice

adf.test(BP_volume_return$volume)
#passed

plot((BP_volume_return$volume-mean(BP_volume_return$volume))/sd(BP_volume_return$volume),type="l",col="black",ylim=c(0,100),main="BP_volume_return(red=std_return,black=std_volume)",ylab="")
par(new=TRUE)
plot((BP_volume_return$return-mean(BP_volume_return$return))/sd(BP_volume_return$return),type="l",col="red",ylim=c(-50,50),axes=F,ylab="")
axis(side=4, col.axis="black")

#########################################################

#RDSA
kurtosis(RDSA_volume_return$volume)
#550.085

mean(RDSA_volume_return$volume)
#6893.807

sd(RDSA_volume_return$volume)
#9372.829

cor(RDSA_volume_return$volume,sqrt(RDSA_volume_return$return^2))
#0.3639852
# need to notice

adf.test(RDSA_volume_return$volume)
#passed

plot((RDSA_volume_return$volume-mean(RDSA_volume_return$volume))/sd(RDSA_volume_return$volume),type="l",col="black",ylim=c(0,100),main="RDSA_volume_return(red=std_return,black=std_volume)",ylab="")
par(new=TRUE)
plot((RDSA_volume_return$return-mean(RDSA_volume_return$return))/sd(RDSA_volume_return$return),type="l",col="red",ylim=c(-50,50),axes=F,ylab="")
axis(side=4, col.axis="black")

#########################################################


