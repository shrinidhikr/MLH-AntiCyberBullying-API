from flask import Flask
from flask_restful import reqparse,Api,Resource 
import pandas as pd
import re
#from json import dumps
#nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from sklearn.feature_extraction.text import CountVectorizer

parser=reqparse.RequestParser()
parser.add_argument('query')

class PredictSentiment(Resource):
    def get(self):
        dataset1 = pd.read_csv('/home/shrinidhikr/Downloads/fwdlocalhackdsay/train.csv' , encoding='cp437')
        y=dataset1.iloc[:,0].values
    
        orpus=[]
        for i in range(0,3947):
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
        #X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 0)
        
        classifier1=RandomForestClassifier(n_estimators=50,criterion='entropy')
        classifier1.fit(x,y)
        i=0
        predRF=[]
        args=parser.parse_args()
        st=args['query']
        st = pd.Series(st)
        predy=cv.transform(st).toarray()
        if(classifier1.predict(predy)==0):
            predRF.append('Not bullying')
        else:
            predRF.append('Bullying')
        """
        s='Accuracy score: {}'.format(accuracy_score(y_test, predRF))
        s1='Precision score: {}'.format(precision_score(y_test, predRF))
        s2='Recall score: {}'.format(recall_score(y_test, predRF))
        s3='F1 score: {}'.format(f1_score(y_test, predRF))
        """
        #j={"A":s,"B":s1,"C":s2,"D":s3}
        pf=""
        for v in predRF:
            pf=pf+str(v)+" "
        #jp=str(j)
        return(pf)
       # print(type(j))

app = Flask(__name__)
api = Api(app)
api.add_resource(PredictSentiment, '/')

if __name__=="__main__":
 app.run(debug=True)

