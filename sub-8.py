#Predicting Outlest sales based on 
# - Item_Visibility
# - Item_MRP
# - Outlet_Establishment Year
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation, metrics
train = pd.read_csv("train_modified.csv")
test = pd.read_csv("test_modified.csv")

def modelfit(alg, dtrain, dtest, predictors, target, IDcol, filename):
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain[target])
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    #Perform cross-validation:
    cv_score = cross_validation.cross_val_score(alg, dtrain[predictors], dtrain[target], cv=20, scoring='neg_mean_squared_error')
    cv_score = np.sqrt(np.abs(cv_score))
    
    #Print model report:
    print("\nModel Report")
    print("RMSE : %.4g" % np.sqrt(metrics.mean_squared_error(dtrain[target].values, dtrain_predictions)))
    print("CV Score : Mean - %.4g | Std - %.4g | Min - %.4g | Max - %.4g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))
    
    #Predict on testing data:
    dtest[target] = alg.predict(dtest[predictors])
    
    #Export submission file:
    IDcol.append(target)
    submission = pd.DataFrame({ x: dtest[x] for x in IDcol})
    submission.to_csv(filename, index=False)

#Define target and ID columns:
target = 'Item_Outlet_Sales'
IDcol = ['Item_Identifier','Outlet_Identifier']
Unusedcol = ['Outlet_Type','Outlet_Location_Type','Outlet_Size','Item_Fat_Content'
        ,'Item_Type','Item_Weight','Outlet_Size']

from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
predictors = [x for x in train.columns if x not in [target]+IDcol]
alg5 = BaggingRegressor(n_estimators=400,n_jobs=-1,base_estimator=DecisionTreeRegressor())
modelfit(alg5, train, test, predictors, target, IDcol, 'alg8.csv')
coef5 = pd.Series(alg5.feature_importances_, predictors).sort_values(ascending=False)
coef5.plot(kind='bar', title='Feature Importances')
