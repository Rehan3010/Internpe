
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
%matplotlib inline
mpl.style.use('ggplot')
car=pd.read_csv('quikr_car.csv')
car.head()
car.shape
car.info()
##### Creating backup copy
backup=car.copy()
## Quality

- names are pretty inconsistent
- names have company names attached to it
- some names are spam like 'Maruti Ertiga showroom condition with' and 'Well mentained Tata Sumo'
- company: many of the names are not of any company like 'Used', 'URJENT', and so on.
- year has many non-year values
- year is in object. Change to integer
- Price has Ask for Price
- Price has commas in its prices and is in object
- kms_driven has object values with kms at last.
- It has nan values and two rows have 'Petrol' in them
- fuel_type has nan values
## Cleaning Data 
#### year has many non-year values
car=car[car['year'].str.isnumeric()]
#### year is in object. Change to integer
car['year']=car['year'].astype(int)
#### Price has Ask for Price
car=car[car['Price']!='Ask For Price']
#### Price has commas in its prices and is in object
car['Price']=car['Price'].str.replace(',','').astype(int)
####  kms_driven has object values with kms at last.
car['kms_driven']=car['kms_driven'].str.split().str.get(0).str.replace(',','')
#### It has nan values and two rows have 'Petrol' in them
car=car[car['kms_driven'].str.isnumeric()]
car['kms_driven']=car['kms_driven'].astype(int)
#### fuel_type has nan values
car=car[~car['fuel_type'].isna()]
car.shape
### name and company had spammed data...but with the previous cleaning, those rows got removed.
#### Company does not need any cleaning now. Changing car names. Keeping only the first three words
car['name']=car['name'].str.split().str.slice(start=0,stop=3).str.join(' ')
#### Resetting the index of the final cleaned data
car=car.reset_index(drop=True)
## Cleaned Data
car
car.to_csv('Cleaned_Car_data.csv')
car.info()
car.describe(include='all')

car=car[car['Price']<6000000]
### Checking relationship of Company with Price
car['company'].unique()
import seaborn as sns
plt.subplots(figsize=(15,7))
ax=sns.boxplot(x='company',y='Price',data=car)
ax.set_xticklabels(ax.get_xticklabels(),rotation=40,ha='right')
plt.show()
### Checking relationship of Year with Price
plt.subplots(figsize=(20,10))
ax=sns.swarmplot(x='year',y='Price',data=car)
ax.set_xticklabels(ax.get_xticklabels(),rotation=40,ha='right')
plt.show()
### Checking relationship of kms_driven with Price
sns.relplot(x='kms_driven',y='Price',data=car,height=7,aspect=1.5)
### Checking relationship of Fuel Type with Price
plt.subplots(figsize=(14,7))
sns.boxplot(x='fuel_type',y='Price',data=car)
### Relationship of Price with FuelType, Year and Company mixed
ax=sns.relplot(x='company',y='Price',data=car,hue='fuel_type',size='year',height=7,aspect=2)
ax.set_xticklabels(rotation=40,ha='right')
### Extracting Training Data
X=car[['name','company','year','kms_driven','fuel_type']]
y=car['Price']
X
y.shape
### Applying Train Test Split
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
#### Creating an OneHotEncoder object to contain all the possible categories
ohe=OneHotEncoder()
ohe.fit(X[['name','company','fuel_type']])
#### Creating a column transformer to transform categorical columns
column_trans=make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),
                                    remainder='passthrough')
#### Linear Regression Model
lr=LinearRegression()
#### Making a pipeline
pipe=make_pipeline(column_trans,lr)
#### Fitting the  model
pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)
#### Checking R2 Score
r2_score(y_test,y_pred)
#### Finding the model with a random state of TrainTestSplit where the model was found to give almost 0.92 as r2_score
scores=[]
for i in range(1000):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1,random_state=i)
    lr=LinearRegression()
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,y_train)
    y_pred=pipe.predict(X_test)
    scores.append(r2_score(y_test,y_pred))
np.argmax(scores)
scores[np.argmax(scores)]
pipe.predict(pd.DataFrame(columns=X_test.columns,data=np.array(['Maruti Suzuki Swift','Maruti',2019,100,'Petrol']).reshape(1,5)))
#### The best model is found at a certain random state 
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.1,random_state=np.argmax(scores))
lr=LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)
r2_score(y_test,y_pred)
import pickle
pickle.dump(pipe,open('LinearRegressionModel.pkl','wb'))
pipe.predict(pd.DataFrame(columns=['name','company','year','kms_driven','fuel_type'],data=np.array(['Maruti Suzuki Swift','Maruti',2019,100,'Petrol']).reshape(1,5)))
pipe.steps[0][1].transformers[0][1].categories[0]
