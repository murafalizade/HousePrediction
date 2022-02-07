from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from sklearn.preprocessing  import LabelEncoder
from sklearn.model_selection import train_test_split
import xgboost as xg



def predictBina(ar,rm,fl,cfl,ll,typ):
    if typ=='kiraye':
        df = pd.read_sql("""SELECT * FROM rent_estate""",con='oracle://murad99:asd@localhost:1521')
    else:
        df = pd.read_sql("""SELECT * FROM estate""",con='oracle://murad99:asd@localhost:1521')
    df = df.drop(['index'],axis=1) 
    df['Floor'] = df['Floor'].fillna("0/0",axis=0)
    df.loc[df['Area']>40,'Rooms'] = 2
    df.loc[df['Area']>60,'Rooms'] = 3
    df.loc[df['Area']>90,'Rooms'] = 4
    df.loc[df['Area']>130,'Rooms'] = 5
    df.loc[df['Area']<=40,'Rooms'] = 1
    df.loc[df['Rooms']>5,'Rooms'] = 5
    floors = []
    current_floor = []
    for x in np.array(df['Floor']):
        current_floor.append(int(x.split('/')[0]))
        floors.append(int(x.split('/')[1]))
    df = df.assign(Floors = floors,Current_floor = current_floor)
    df = df.drop(['Floor'],axis=1)
    scaler = LabelEncoder()
    df['LocationLabel'] = scaler.fit_transform(df['Locations'])
    X = df.drop(['Locations','Prices'],axis=1)
    y = df['Prices']
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=123)
    xgb_r = xg.XGBRegressor(objective ='reg:squarederror',
                    n_estimators = 10, seed = 123)
    xgb_r.fit(X_train, y_train)
    try:
        ll = np.array(df[df['Locations']==ll]['LocationLabel'])[0]
    except:
        ll = np.max(np.array(df['LocationLabel']))+1
    pred = xgb_r.predict(pd.DataFrame({'Area':[ar],'Rooms':[rm],'Floor':[fl],'Current_floor':[cfl],"LocationLabel":[ll]}))
    return pred[0]
#print(predictBina(40,2,1,1,'Qusar'))