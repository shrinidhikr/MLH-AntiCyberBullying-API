import pandas as pd 
#import os
#import json
from sklearn.feature_extraction.text import CountVectorizer    
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

'''#Data Cleaning and Preprocessing'''
dataset1 = pd.read_csv('test_with_solutions.csv' , encoding='cp437')
y=dataset1.iloc[:,0].values
orpus=[]
for i in range(0,2647):
    review = re.sub('[^a-zA-Z]',' ',dataset1['Comment'][i])
    review=review.lower()
    review=review.split()
    ps=PorterStemmer()
    review=[ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review=' '.join(review)
    orpus.append(review)

cv=CountVectorizer(max_features=3000)
x=cv.fit_transform(orpus).toarray()

le=LabelEncoder()
y=le.fit_transform(y)   

'''#Splitting the dataset into the Training set and Test set'''
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 0)

#from sklearn.naive_bayes import GaussianNB
#classifier=GaussianNB()
#classifier.fit(X_train,y_train)
#predition
#pred=classifier.predict(X_test)
#print(pred)
#from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
#print('Accuracy score: {}'.format(accuracy_score(y_test, pred)))
#print('Precision score: {}'.format(precision_score(y_test, pred)))
#print('Recall score: {}'.format(recall_score(y_test, pred)))
#print('F1 score: {}'.format(f1_score(y_test, pred)))'''

'''#Model training'''
classifier1=RandomForestClassifier(n_estimators=20,criterion='entropy')
classifier1.fit(X_train,y_train)
predRF=classifier1.predict(X_test)

print('Accuracy score: {}'.format(accuracy_score(y_test, predRF)))
print('Precision score: {}'.format(precision_score(y_test, predRF)))
print('Recall score: {}'.format(recall_score(y_test, predRF)))
print('F1 score: {}'.format(f1_score(y_test, predRF)))


cm = confusion_matrix(y_test, predRF)
print(cm)

print(predRF)
