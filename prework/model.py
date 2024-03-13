import itertools
import os
import numpy as np
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt


# Takes the folder path as input and returns the path to the latest CSV file in that folder.
def get_latest_csv_file(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Sort the CSV files based on their timestamps
    sorted_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    
    if sorted_files:
        # Return the path to the latest CSV file
        return os.path.join(folder_path, sorted_files[0])
    else:
        return None

# Load the dataset
folder_path = 'prework/data'
latest_csv_file = get_latest_csv_file(folder_path)
if latest_csv_file:
    print("Latest CSV file: " + latest_csv_file)
    df = pd.read_csv(latest_csv_file)
else:
    print("No CSV files found in the folder.")
    
# Assign features (X) and target labels (y)
X = df.iloc[:, 1:-1]  # Select all columns except the last one as features
y = df.iloc[:, -1]   # Select the last column as the target

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=35)

# Creating the Decision Tree Classifier
clf = DecisionTreeClassifier()

# Fitting the classifier to the training data
clf.fit(X_train, y_train)

# Making predictions on the testing data
y_pred = clf.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Feature importances
feature_importances = pd.Series(clf.feature_importances_, index=X.columns)

# Plotting feature importances as a bar chart
plt.figure(figsize=(10, 6))
feature_importances.plot(kind='bar')
plt.title('Feature Importances')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.xticks(rotation=45)
plt.show()

# Visualizing the decision tree
plt.figure(figsize=(12, 8))
class_names = np.unique(y).astype(str)
plot_tree(clf, filled=True, feature_names=X.columns, class_names=class_names)
plt.show()


# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Plotting confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(len(np.unique(y)))
plt.xticks(tick_marks, np.unique(y))
plt.yticks(tick_marks, np.unique(y))

fmt = '.2f' if normalize else 'd'
thresh = conf_matrix.max() / 2.
for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
    plt.text(j, i, format(conf_matrix[i, j], fmt),
             horizontalalignment="center",
             color="white" if conf_matrix[i, j] > thresh else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()
