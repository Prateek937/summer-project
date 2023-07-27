import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder
#from sklearn.metrics import confusion_matrix
#import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error
from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import train_test_split
#from sklearn import metrics
from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import LogisticRegression
#from sklearn.model_selection import train_test_split
def train_your_model():
    data = input("Enter your dataset: ")
    dataset=pd.read_csv(data)
    print(dataset.columns)
    dg=input("Enter your target column: ")
    y=dataset[[dg]]
    dataset.drop(dg,axis=1,inplace=True)
    dummies = pd.DataFrame()
    #print(dummies)
    for i in range(0,len(dataset.columns)):
        temp = dataset.columns[i]
        l1 = list(set(list(dataset[temp])))
        #print(len(l1))
        if len(l1) <= 2*(len(dataset[dataset.columns[i]].values))/100:
            dummies = pd.concat((dummies,  pd.get_dummies(dataset[dataset.columns[i]],drop_first=True)), axis=1)
        else :
            if type(list(dataset[dataset.columns[i]])[1]) == str:
                pass
            else:
                #print("Error")
                #temp = dataset.iloc[:, i].to_frame()
                dummies = pd.concat((dummies ,dataset.iloc[:, i].to_frame()),axis = 1)
    dataset = dummies
    dataset = pd.concat((dummies,  y), axis=1)
    for i in range(0,len(dataset.columns)-1):
        try:
            if type(dataset.columns[i]) == str:
                relation = dataset[dg].corr(dataset[dataset.columns[i]])
                #print(dataset.columns[i])
                #print(relation)
                if relation > (-0.05) :
                    dataset.drop(dataset.columns[i],axis=1,inplace=True)
                else:
                    pass
        except:
            pass
    for i in range(0,len(dataset.columns)):
        if type(dataset.columns[i]) == str:
                count=dataset[dataset.columns[i]].mean()
                dataset[dataset.columns[i]].fillna(value = count, inplace=True)

    dataset.columns=dataset.columns.astype(str)
    x=dataset

    if len(set(list(y[dg]))) < (2*len(y)/100):
        if len(set(list(y[dg]))) == 2:
            #Simple Logistics Regression
            x_train,x_test,y_train,y_test=train_test_split( x, y, test_size=0.20, random_state=42)
            model=LogisticRegression()
            #model.fit(x,y)
            model.fit(x_train,y_train)
            print(model.coef_)
            print(model.intercept_)    
            y_pred=model.predict(x_test)
            print(confusion_matrix(y_test,y_pred))
            accuracy = accuracy_score(y_test, y_pred)
            print("Accuracy:", accuracy)

            conf_matrix = confusion_matrix(y_test, y_pred)
            print("Confusion Matrix:\n", conf_matrix)

            class_report = classification_report(y_test, y_pred)
            print("Classification Report:\n", class_report)
            #print(len(set(list(y[myy]))))  
            #sigmoid
        else:
            #Multilogistics Regression
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print("Accuracy:", accuracy)

            conf_matrix = confusion_matrix(y_test, y_pred)
            print("Confusion Matrix:\n", conf_matrix)

            class_report = classification_report(y_test, y_pred)
            print("Classification Report:\n", class_report)
    else:
        if len(x.columns) == 1 :
            #Simple linear Regression
            model=LinearRegression()
            model.fit(x,y)
            y_pred = model.predict(x)
            print("Coefficient: ", model.coef_)
            print("Intercept:", model.intercept_)
            print("Mean Absolute Error: ", mean_absolute_error(y,y_pred))
        else:
            #Multilinear Regression
            model=LinearRegression()
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=5)
            model.fit(x_train,y_train)
            y_pred = model.predict(x_test)
            print("Coefficient: ", model.coef_)
            print("Mean Absolute Error: ", mean_absolute_error(y_test,y_pred))

train_your_model()