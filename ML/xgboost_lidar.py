import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from micromlgen import port

def letters_to_colors(letters):
    color_mapping = {
        'F': 'blue',
        'G': 'cyan',
        'I': 'magenta'
    }
    
    return [color_mapping.get(letter, 'black') for letter in letters]

# read data from csv
data = pd.read_csv('../data/test4567.txt', header=None)
data.rename(columns={data.columns[-1]: 'Label'}, inplace=True)
data = data[(data['Label'] != 'L') & (data['Label'] != 'R') & (data['Label'] != 'H')]
data.reset_index(drop=True, inplace=True)

X = data.iloc[:, :-1]
# Assign target y as the last column 'Label'
y = data.iloc[:, -1]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Use LDA to select the top 2 features
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X_train, y_train)

# Use the best hyperparameters to fit the model
xgb_best = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.01,
    subsample=0.5,
    colsample_bytree=1.0
    )
xgb_best.fit(X_lda, y_train)

# Use the model to make predictions on the test set
X_test_lda = lda.transform(X_test)
y_pred = xgb_best.predict(X_test_lda)

# Calculate the accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"The accuracy score of the Random Forest classifier with LDA feature selection is {accuracy:.2f}.")

class_names = label_encoder.classes_
report = classification_report(y_test, y_pred, target_names=class_names, zero_division=0)
print('Classification Report:\n', report)

arduino_code = open("arduino_random_forest5.c", mode="w+")
arduino_code.write(port(xgb_best))