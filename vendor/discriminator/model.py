import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn
import string
from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import learning_curve
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier


import sklearn.gaussian_process.kernels as kernels

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

from scipy.stats import expon


payloads = pd.read_csv("/data/payloads.csv",index_col='index')
# print(payloads.head(30))


def create_feature_length(payloads):
    payloads['length'] = [len(str(row)) for row in payloads['payload']]
    return payloads

def create_feature_non_printable_characters(payloads):  
    payloads['non-printable'] = [ len([1 for letter in str(row) if letter not in string.printable]) for row in payloads['payload']]
    return payloads
    
def create_feature_punctuation_characters(payloads):
    payloads['punctuation'] = [ len([1 for letter in str(row) if letter in string.punctuation]) for row in payloads['payload']]
    return payloads

def create_feature_min_byte_value(payloads):
    payloads['min-byte'] = [ min(bytearray(str(row), 'utf8')) for row in payloads['payload']]
    return payloads

def create_feature_max_byte_value(payloads):
    payloads['max-byte'] = [ max(bytearray(str(row), 'utf8')) for row in payloads['payload']]
    return payloads

def create_feature_mean_byte_value(payloads):
    payloads['mean-byte'] = [ np.mean(bytearray(str(row), 'utf8')) for row in payloads['payload']]
    return payloads

def create_feature_std_byte_value(payloads):
    payloads['std-byte'] = [ np.std(bytearray(str(row), 'utf8')) for row in payloads['payload']]
    return payloads

def create_feature_distinct_bytes(payloads):
    payloads['distinct-bytes'] = [ len(list(set(bytearray(str(row), 'utf8')))) for row in payloads['payload']]
    return payloads

sql_keywords = pd.read_csv('/content/drive/My Drive/WAF/data/SQLKeywords.txt', index_col=False)

def create_feature_sql_keywords(payloads):
    payloads['sql-keywords'] = [ len([1 for keyword in sql_keywords['Keyword'] if str(keyword).lower() in str(row).lower()]) for row in payloads['payload']]
    return payloads

js_keywords = pd.read_csv('/content/drive/My Drive/WAF/data/JavascriptKeywords.txt', index_col=False)

def create_feature_javascript_keywords(payloads):
    payloads['js-keywords'] = [len([1 for keyword in js_keywords['Keyword'] if str(keyword).lower() in str(row).lower()]) for row in payloads['payload']]
    return payloads
    


def create_features(payloads):
    features = create_feature_length(payloads)
    features = create_feature_non_printable_characters(features)
    features = create_feature_punctuation_characters(features)
    features = create_feature_max_byte_value(features)
    features = create_feature_min_byte_value(features)
    features = create_feature_mean_byte_value(features)
    features = create_feature_std_byte_value(features)
    features = create_feature_distinct_bytes(features)
    features = create_feature_sql_keywords(features)
    features = create_feature_javascript_keywords(features)
    del features['payload']

    return features
# %time create_features(payloads)



def custom_features_assesment():
    Y = payloads['is_malicious']
    X = create_features(pd.DataFrame(payloads['payload'].copy()))


    test = SelectKBest(score_func=chi2, k='all')
    fit = test.fit(X, Y)
    # summarize scores
    print(fit.scores_)
    features = fit.transform(X)
    # summarize selected features
    # summarize scores
    np.set_printoptions(precision=2)
    print(fit.scores_)

    # Get the indices sorted by most important to least important
    indices = np.argsort(fit.scores_)

    # To get your top 10 feature names
    featuress = []
    for i in range(10):
        featuress.append(X.columns[indices[i]])

    display(featuress)
    display([featuress[i] + ' ' + str(fit.scores_[i]) for i in indices[range(10)]])


    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_pos = np.arange(len(featuress))
    performance = 3 + 10 * np.random.rand(len(featuress))
    error = np.random.rand(len(featuress))

    ax.barh(y_pos, fit.scores_[indices[range(10)]],  align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(featuress)
    ax.set_xscale('log')

    #ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Points')
    ax.set_title('SelectKBest()')

    plt.show()

custom_features_assesment()




def get2Grams(payload_obj):
    '''Divides a string into 2-grams
    
    Example: input - payload: "<script>"
             output- ["<s","sc","cr","ri","ip","pt","t>"]
    '''
    payload = str(payload_obj)
    ngrams = []
    for i in range(0,len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams



def train_model(clf, param_grid, X, Y):
    
    #First, partition into train and test data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # n_iter = 5
    # #If number of possible iterations are less than prefered number of iterations, 
    # #set it to the number of possible iterations
    # #number of possible iterations are not less than prefered number of iterations if any argument is expon()
    # #because expon() is continous (writing 100 instead, could be any large number)
    # n_iter = min(n_iter,np.prod([
    #     100 if type(xs) == type(expon()) 
    #     else len(xs) 
    #     for xs in param_grid.values()
    # ]))

    n_iter = 1

    #perform a grid search for the best parameters on the training data.
    #Cross validation is made to select the parameters, so the training data is actually split into
    #a new train data set and a validation data set, K number of times
    cv = ShuffleSplit(n_splits=20, test_size=0.2, random_state=0) #DEBUG: n_iter=10
    #cv = KFold(n=len(X), n_folds=10)
    random_grid_search = RandomizedSearchCV(
        clf, 
        param_distributions=param_grid,
        cv=cv, 
        scoring='f1', 
        n_iter=n_iter, #DEBUG 1 
        random_state=5,
        refit=True,
        verbose=10
    )


    random_grid_search.fit(X_train, Y_train)
    
    #Evaluate the best model on the test data
    Y_test_predicted = random_grid_search.best_estimator_.predict(X_test)
    Y_test_predicted_prob = random_grid_search.best_estimator_.predict_proba(X_test)[:, 1]

    confusion = confusion_matrix(Y_test, Y_test_predicted)
    TP = confusion[1, 1]
    TN = confusion[0, 0]
    FP = confusion[0, 1]
    FN = confusion[1, 0]

    #Calculate recall (sensitivity) from confusion matrix
    sensitivity = TP / float(TP + FN)
    
    #Calculate specificity from confusion matrix
    specificity = TN / float(TN + FP)

    #Calculate accuracy
    accuracy = (confusion[0][0] + confusion[1][1]) / (confusion.sum().sum())
    
    #Calculate axes of ROC curve
    fpr, tpr, thresholds = roc_curve(Y_test, Y_test_predicted_prob)
    
    #Area under the ROC curve
    auc = roc_auc_score(Y_test, Y_test_predicted_prob)

    return {
        'conf_matrix':confusion, 
        'accuracy':accuracy, 
        'sensitivity':sensitivity,
        'specificity':specificity,
        'auc':auc,
        'params':random_grid_search.best_params_,
        'model':random_grid_search.best_estimator_,
        'roc':{'fpr':fpr,'tpr':tpr,'thresholds':thresholds}
    }



count_vectorizer_2grams = CountVectorizer(min_df=1, tokenizer=get2Grams)

classifier_inputs = {
    'pipeline':Pipeline([('vect', count_vectorizer_2grams),('clf',RandomForestClassifier(
        max_depth=None,min_samples_split=2, random_state=0))]),
    'dict_params': {
        'vect__min_df':[1,2,5,10,20,40],
        'clf__n_estimators':[10,20,40,60]
    }
}

X = payloads['payload'] 
Y = payloads['is_malicious']

result_dict = train_model(classifier_inputs['pipeline'],classifier_inputs['dict_params'],X,Y)
# print(result_dict)



import pickle

filename = '/finalized_model.sav'

pickle.dump(result_dict, open(filename, 'wb'))