import pandas as pd
import random

from sklearn import svm, preprocessing, tree
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import recall_score, precision_score, roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier



## Read historical data -- for training
data = pd.read_csv('banknotes_history.csv',index_col=0)

# # if data contains missing value
data = pd.read_csv('banknotes_history_NA.csv',index_col=0)
data = data.dropna(subset=['label'])  # remove banknotes that contains NA value
data = data.fillna(data.mean()) # fill in the banknotes with the column mean

# Prepare the outcome y, and feature dataframe
label = data.pop('label')
train_data=pd.DataFrame(preprocessing.scale(data))


## Build and train a machine learning model
model = KNeighborsClassifier(n_neighbors=1) #nearest neighbor
model = Perceptron() #Perceptron
model = svm.SVC() # support vector machine
model = tree.DecisionTreeClassifier() # decision trees
model = RandomForestClassifier(n_estimators=10) # random forest
model = GaussianNB() #Naive Bayes


model.fit(train_data, label)


## Make prediction
# read data
pred = pd.read_csv('banknotes_new.csv',index_col=0)
index = pred.index

#process data
pred=pd.DataFrame(preprocessing.scale(pred))
pred.index=index

#make prediction
outcome=pd.DataFrame(model.predict(pred))
# model.decision_function(pred)
outcome.index=index
outcome.columns=['predicted']


## Evaluate the performance
actual=pd.read_csv('banknotes_new_result.csv',index_col=0)
outcome=outcome.merge(actual,left_index=True,right_index=True,how='inner')

# Compute how well we performed
correct = 0
incorrect = 0
total = 0
for actual, predicted in zip(outcome.label, outcome.predicted):
    total += 1
    if actual == predicted:
        correct += 1
    else:
        incorrect += 1

sensitivity=recall_score(outcome.label, outcome.predicted, pos_label=1)
specificity=recall_score(outcome.label, outcome.predicted, pos_label=0)
precision = precision_score(outcome.label, outcome.predicted)
F1Score = f1_score(outcome.label, outcome.predicted)
auc = roc_auc_score(outcome.label, outcome.predicted)

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")
print(f"Sensitivity/Recall: {100 * sensitivity:.2f}%")
print(f"Specificity: {100 * specificity:.2f}%")
print(f"Precision: {100 * precision:.2f}%")
print(f"F1 score: {F1Score:.4f}")
print(f"AUC: {auc:.4f}")



### if want to split training and testing dataset

X_training, X_testing, y_training, y_testing = train_test_split(
    data, label, test_size=0.4
)
X_training
y_training

model.fit(X_training, y_training)

# Make predictions on the testing set
predictions = model.predict(X_testing)

# Compute how well we performed
correct = (y_testing == predictions).sum()
incorrect = (y_testing != predictions).sum()
total = len(predictions)
sensitivity=recall_score(y_testing,predictions, pos_label=1)
specificity=recall_score(y_testing,predictions, pos_label=0)
precision = precision_score(y_testing,predictions)
F1Score = f1_score(y_testing,predictions)
auc = roc_auc_score(y_testing,predictions)
# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")
print(f"Sensitivity: {100 * sensitivity:.2f}%")
print(f"Specificity: {100 * specificity:.2f}%")
print(f"Precision: {100 * precision:.2f}%")
print(f"F1 score: {F1Score:.4f}")
print(f"AUC: {auc:.4f}")


## k-fold cross validation
scores = cross_val_score(model, train_data, label, cv=5) # five-fold cross validation
scores # accuracy

