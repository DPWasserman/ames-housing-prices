install.packages("xlsx")

library(foreign)
library("xlsx")
library(glmnet)
library(ggplot2)

rm(list=ls())
train = read.csv("/Users/janruffner/Desktop/ProjectMachineLearning/ames-housing-prices/Data/Ames_Housing_Price_Data.csv", sep=",")

str(train)

#Clean Data
# SalePrice
train$LogSalePrice = log(train$SalePrice)
train$SalePrice_LotArea=train$SalePrice/train$GrLivArea
train$LogSalePrice_LotArea=log(train$SalePrice_LotArea)



# Deal with missings

# Columns with missing variables:
colnames(train)[colSums(is.na(train)) > 0]
# LotFrontage: Replace NAs with Mean
train[is.na(train$LotFrontage),"LotFrontage"]=0
# Alley: Replace NAs with NoAlley
train[is.na(train$Alley), "Alley"] <- "NoAlley"
# MasVnrType: No important variable   
# MasVnrArea: Replace NAs with 0
train[is.na(train$MasVnrArea), "MasVnrArea"] <- 0
# BsmtQual: Replace NAs with NoBasement
train[is.na(train$BsmtQual), "BsmtQual"] <- "NoBasement"
# BsmtCond: Replace NAs with NoBasement
train[is.na(train$BsmtCond), "BsmtCond"] <- "NoBasement"
# BsmtExposure: Replace NAs with NoBasement
train[is.na(train$BsmtExposure), "BsmtExposure"] <- "NoBasement"
# BsmtFinType1:Replace NAs with NoBasement
train[is.na(train$BsmtFinType1), "BsmtFinType1"] <- "NoBasement"
# BsmtFinType2:Replace NAs with NoBasement
train[is.na(train$BsmtFinType2), "BsmtFinType2"] <- "NoBasement"
# FireplaceQu: I don't think this variable is important
# GarageType: Replace NAs with NoGarage
train[is.na(train$GarageType), "GarageType"] <- "NoGarage"
# GarageYrBlt: Replace NAs with YearBuilt
train[is.na(train$GarageYrBlt), "GarageYrBlt"] <- train[is.na(train$GarageYrBlt), "YearBuilt"]
# GarageFinish: Replace NAs with NoGarage
train[is.na(train$GarageFinish), "GarageFinish"] <- "NoGarage"
# GarageQual: Replace NAs with NoGarage
train[is.na(train$GarageQual), "GarageQual"] <- "NoGarage"
# GarageCond: Replace NAs with NoGarage
train[is.na(train$GarageCond), "GarageCond"] <- "NoGarage"
# PoolQC: No important variable. Just 7 observations 
sum(!is.na(train$PoolQC))
# Fence:No important variable-drop        
# MiscFeature: Replace NA with NoFeature
train[is.na(train$MiscFeature), "MiscFeature"] <- "NoFeature"
# Electrical: Replace missing with most common electrical system
train[is.na(train$Electrical), "Electrical"] <- "SBrkr"


# Drop Variables:
train <- train %>% select(-c("Fence","FireplaceQu", "PoolQC") )

# Creating Variables
# Age
train$age=2011-train$YearBuilt
# Age2
train$age2=train$age^2
# GarageYesNo
train$GarageYesNo <- ifelse(train$GarageType=="NoGarage", 0, 1)
# AlleyYesNo
train$AlleyYesNo <- ifelse(train$Alley=="NoAlley", 0, 1)
# BasementYesNo
train$BasementYesNo <- ifelse(train$BsmtQual=="NoBasement", 0, 1)
# Second Garage
train$Gar2 <- ifelse(train$MiscFeature=="Gar2", 1, 0)
# Shed
train$ShedYesNo <- ifelse(train$MiscFeature=="Shed", 1, 0)
# 
train$Neighborhood <- as.factor(train$Neighborhood)
train$Neighborhood2 <- ifelse(train$Neighborhood=="NridgHt" | train$Neighborhood=="NoRidge" | train$Neighborhood=="StoneBr", 1, 
                        ifelse(train$Neighborhood=="Timber" | train$Neighborhood=="Somerst" | train$Neighborhood=="Veenker", 2, 
                        ifelse(train$Neighborhood=="Crawfor" | train$Neighborhood=="ClearCr" | train$Neighborhood=="CollgCr"
                                      | train$Neighborhood=="Blmngtn" | train$Neighborhood=="NWAmes" | train$Neighborhood=="Gilbert" | train$Neighborhood=="SawyerW", 3,
                        ifelse(train$Neighborhood=="Mitchel" | train$Neighborhood=="NPkVill" | train$Neighborhood=="NAmes"
                               | train$Neighborhood=="SWISU" | train$Neighborhood=="Blueste" | train$Neighborhood=="Sawyer", 4,
                               ifelse(train$Neighborhood=="BrkSide" | train$Neighborhood=="Edwards" | train$Neighborhood=="OldTown", 5, 
                                      ifelse(train$Neighborhood=="BrDale" | train$Neighborhood=="IDOTRR", 6,7))))))
train %>% select(Neighborhood, Neighborhood2)
train$Neighborhood2 <- as.factor(train$Neighborhood2)

########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


# Analyzing SalePrice Data
ggplot(data=train)+geom_density(aes(SalePrice))+ggtitle("Density Plot of Sale Price")+xlab("Sale Price")+ylab("Density")
ggplot(data=train)+geom_density(aes(LogSalePrice))+ggtitle("Density Plot of Log Sale Price")+xlab("Log Sale Price")+ylab("Density") #Log Sale Price looks normally distributed
ggplot(data=train)+geom_density(aes(SalePrice_LotArea)) #Sale Price/per sqm does not look normally distributed
ggplot(data=train)+geom_density(aes(LogSalePrice_LotArea)) # Log Sale Price looks normally distributed

#Korrelation Matrix
data <- cor(train[, c("LogSalePrice",
              "MSSubClass",
              "YearBuilt",
              "YearRemodAdd",
              "LotFrontage", 
              "LotArea", 
              "OverallQual",
              "OverallCond",
              "MasVnrArea",
              "BsmtFinSF1",
              "BsmtFinSF2",
              "BsmtUnfSF",
              "TotalBsmtSF",
              "X1stFlrSF",
              "LowQualFinSF", 
              "GrLivArea",
              "BsmtFullBath",
              "BsmtHalfBath",
              "FullBath",
              "HalfBath",
              "BedroomAbvGr",
              "KitchenAbvGr",
              "TotRmsAbvGrd",
              "TotRmsAbvGrd",
              "GarageYrBlt",
              "WoodDeckSF",
              "OpenPorchSF",
              "EnclosedPorch",
              "X3SsnPorch",
              "ScreenPorch")], use="complete.obs")
cor <- data["LogSalePrice",]
cor <- cor[order(cor, decreasing = TRUE)]

# Analyzing variables - SquareFeet
SquareFeet <- train[, c("LotFrontage", 
                        "LotArea", 
                        "MasVnrArea",
                        "BsmtFinSF1",
                        "BsmtFinSF2",
                        "BsmtUnfSF",
                        "TotalBsmtSF",
                        "X1stFlrSF",
                        "LowQualFinSF", 
                        "GrLivArea",
                        "WoodDeckSF",
                        "OpenPorchSF",
                        "EnclosedPorch")]
cor(SquareFeet)

# Analyzing variables - Number of Rooms

# Analyzing variables - Sale
Sale <- train[, c("YrSold", 
                        "MoSold", 
                        "SaleCondition",
                        "SaleType")]


# Analyzing variables - Year Built / Year Remodelled
YearBuilt <- train[, c("YearBuilt", 
                  "YearRemodAdd", 
                  "GarageYrBlt")]
cor(YearBuilt, use="complete.obs") 


# Analyzing Variables - Quality
ggplot(train, aes(x=as.factor(OverallQual), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(FireplaceQu), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(PoolQC), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(Fence), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(HeatingQC), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(KitchenQual), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()

Quality <- train[, c("OverallQual", 
                     "HeatingQC",
                     "KitchenQual")]

# Analyzing Variables - Condition
ggplot(train, aes(x=reorder(as.factor(OverallCond), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(GarageCond), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(BsmtCond), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()
ggplot(train, aes(x=reorder(as.factor(ExterCond), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()


# Number Of Rooms, Number of apartements
# Floor Level
# MicroLocation
ggplot(train, aes(x=reorder(as.factor(Neighborhood), LogSalePrice, FUN = median), y=LogSalePrice)) + geom_boxplot()



# What should be included for sure in regression: 
# Dwelling Area (ok), Age in Year (ok), Age in Years Squared (ok), Number of Rooms, Number of apartements, Floor Level, Condition (ok), Standard (ok), 
# Micro-location, mixed building

########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


######################################
###### Linear Regression #############
######################################

reg1 <- lm(LogSalePrice ~ age + age2 + LotArea + OverallCond + OverallQual + GrLivArea + BedroomAbvGr  +Neighborhood2 + MSZoning + Condition1 + Condition2+BasementYesNo , data=train)
summary(reg1)
mean((predict(reg1)-train$LogSalePrice)^2)
rmse(train$LogSalePrice, predict(reg1, train))

reg2 <- lm(LogSalePrice ~ age + age2 + LotArea + OverallCond + OverallQual + GrLivArea + BedroomAbvGr  +Neighborhood + MSZoning + Condition1 + Condition2+BasementYesNo+HouseStyle , data=train)
summary(reg2)
mean((predict(reg2)-train$LogSalePrice)^2)
rmse(train$LogSalePrice, predict(reg2, train))

#### Cross Validation
y = train$LogSalePrice
x = train %>% select(age, age2, LotArea, OverallCond, OverallQual, GrLivArea, BedroomAbvGr, Neighborhood2, MSZoning, Condition1, Condition2, BasementYesNo)
x <- data.matrix(x)

cv.models = cv.glmnet(x, y, nfolds=5)
besttrain = predict(cv.models, newx = x)
mean((besttrain - y)^2) 
rmse(y, besttrain)

#### Cross Validation/Lasso
grid <- 10^seq(5, -2, length = 100)
set.seed(0)

lasso.models = glmnet(x, y, alpha = 1, lambda = grid)
plot(lasso.models, xvar = "lambda", label = TRUE, main = "Lasso Regression")

cv.lasso.models = cv.glmnet(x, y, alpha = 1,  lambda = grid, nfolds=5)
plot(reg2, xvar = "lambda", label = TRUE, main = "Lasso Regression")

# Optimal Lambda
log(cv.lasso.models$lambda.min)
bestlambda.ridge = cv.lasso.models$lambda.min

# Fit model to data
ridge.bestlambdatrain = predict(lasso.models, s = bestlambda.ridge, newx = x)
mean((ridge.bestlambdatrain - y)^2) 
rmse(y, ridge.bestlambdatrain)

######################################
###### support vector regression ####
######################################


######################################
###### random forest #################
######################################
library(ggplot2)
library(cowplot)
library(randomForest)

y = train$LogSalePrice
x = train %>% select(age, age2, LotFrontage, LotArea, OverallCond, OverallQual, GrLivArea, BedroomAbvGr, Neighborhood2)
x <- as.matrix(x)

set.seed(0)
rf <- randomForest(LogSalePrice ~ age + age2 + LotFrontage + LotArea + OverallCond + OverallQual + GrLivArea + BedroomAbvGr  +Neighborhood + MSZoning + Condition1 + Condition2,
                   data=train, ntree=50, mtry=4, proximity=TRUE)


summary(rf)
mean((predict(rf)-train$LogSalePrice)^2)
rmse(train$LogSalePrice, predict(rf, train))

#Importance of the variables
varImpPlot(rf, 
           sort=T,
           main = "Variable Importance")

### Error Rate
plot(rf)

#Tune mtry
oobs.values <- vector(length=5)
for (i in 1:5) {
  set.seed(0)
  temp.model <- randomForest(LogSalePrice ~ age + age2 + LotFrontage + LotArea + OverallCond + OverallQual + GrLivArea + BedroomAbvGr  +Neighborhood + MSZoning + Condition1 + Condition2,
                             data=train, ntree=50, mtry=i, proximity=TRUE)
  oobs.values[i] <- mean((predict(temp.model)-train$LogSalePrice)^2)
}

#No. of nodes for the trees
hist(treesize(rf),
     main ="No. of Nodes for the Trees",
     col = "green")

# Cross validation
library(caret)
set.seed(0)
cv.10.folds <- createMultiFolds(train$LogSalePrice, k=10, times=10)
ctrl.1 <- trainControl(method="repeatedcv", number=10, repeats=10, index=cv.10.folds)

y = train$LogSalePrice
x = train %>% select(age, age2, LotFrontage, LotArea, OverallCond, OverallQual, GrLivArea, BedroomAbvGr, Neighborhood2)
x <- data.matrix(x)

rf2 <- train(x=x, y=y, method="rf", tuneLength=4, ntree=40, trControl=ctrl.1)

besttrain = predict(rf2, newx = x)
mean((besttrain - y)^2) 
rmse(y, besttrain)

######################################
###### gradient boosting regression ##
######################################





