# TODO Make the model available from within the application
# TODO Try increasing accuracy
# TODO Make the attributes more functional by using various plots, algorithms. Aiming to increase accuracy

import os
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler, normalize
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Takes the folder path as input and returns the path to the latest CSV file in that folder.
def get_latest_csv_file():
    # Get a list of all files in the folder
    files = os.listdir(os.path.join(os.getcwd(), 'data'))
    print(files)

    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    # Sort the CSV files based on their timestamps
    sorted_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join('data', x)), reverse=True)

    if sorted_files:
        # Return the path to the latest CSV file
        return os.path.join('data', sorted_files[0])
    else:
        return None


# Load the dataset
latest_csv_file = get_latest_csv_file()
if latest_csv_file:
    print("Latest CSV file: " + latest_csv_file)
    data = pd.read_csv(latest_csv_file)
else:
    print("No CSV files found in the folder.")

# Let's take a look at the first few rows of the dataset
# print(data.head())

# Check the size of the dataset
# print("Dataset size:", data.shape)

# Get the statistical summary of the dataset
# print("Statistical summary of the dataset:\n", data.describe())

# Drop Image Name column
data = data.drop(columns=['Image_Name'], axis=1)

# Select the categorical columns
categorical_column = ['Target']

# One-hot encoding
encoder = OneHotEncoder(sparse_output=False)
one_hot_encoded = encoder.fit_transform(data[categorical_column])

# Create a dataframe from the one-hot encoded array
one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_column))

# Concatenate the one-hot encoded dataframe with the original dataframe
df_encoded = pd.concat([data, one_hot_df], axis=1)

# Drop the original categorical columns
df_encoded = df_encoded.drop(categorical_column, axis=1)

num_cols = [col for col in df_encoded.columns if
            col not in ['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death']]

min_max_scaler = MinMaxScaler()
df_encoded[num_cols] = min_max_scaler.fit_transform(df_encoded[num_cols])

df_encoded[num_cols] = normalize(df_encoded[num_cols])

standard_scaler = StandardScaler()
df_encoded[num_cols] = standard_scaler.fit_transform(df_encoded[num_cols])

# Let's create a loop to check for outliers
for column in df_encoded.columns[:-3]:
    # Calculate the first and third quartiles
    Q1 = df_encoded[column].quantile(0.25)
    Q3 = df_encoded[column].quantile(0.75)

    # Calculate the lower and upper bounds for outliers
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Detect outliers
    outliers = df_encoded[(df_encoded[column] < lower_bound) | (df_encoded[column] > upper_bound)]

    # Remove rows with outliers completely
    df_encoded = df_encoded.drop(outliers.index)

    # Print out the outliers and their counts and percentages
    #print("{}. Outliers:\n".format(column), outliers)
    #print("{}. Number of Outliers: {}".format(column, outliers.shape[0]))
    #print("{}. Percentage of Outliers: {:.2f}%\n".format(column, outliers.shape[0] / df_encoded.shape[0] * 100))

#print("After removing rows with outliers, the size of the dataset is:", df_encoded.shape)

# Separate independent variables (X) and target variable (y)
X = df_encoded.drop(columns=['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death'])
y = df_encoded[['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Define the parameter grid
# param_grid_decision_tree = {
#     'max_depth': [None, 5, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'criterion': ['gini', 'entropy']
# }
#
# # Define the parameter grid
# param_grid_knn = {
#     'n_neighbors': [3, 5, 7, 9, 11],
#     'weights': ['uniform', 'distance'],
#     'p': [1, 2]  # 1 for Manhattan distance, 2 for Euclidean distance
# }
#
# # Define the parameter grid
# param_grid_random_forest = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'bootstrap': [True, False]
# }

# # Decision Trees
# dt_model = DecisionTreeClassifier()
# # Initialize GridSearchCV
# grid_search = GridSearchCV(dt_model, param_grid_decision_tree, cv=5, scoring='accuracy', n_jobs=-1)
# # Fit the grid search to the data
# grid_search.fit(X_train, y_train)
# # Get the best parameters
# best_params = grid_search.best_params_
# # Use the best model
# best_dt_model = grid_search.best_estimator_
# # Evaluate the best model
# dt_pred = best_dt_model.predict(X_test)
#
# # K-Nearest Neighbors (KNN)
# knn_model = KNeighborsClassifier()
# # Initialize GridSearchCV
# grid_search = GridSearchCV(knn_model, param_grid_knn, cv=5, scoring='accuracy', n_jobs=-1)
# # Fit the grid search to the data
# grid_search.fit(X_train, y_train)
# # Get the best parameters
# best_params = grid_search.best_params_
# # Use the best model
# best_knn_model = grid_search.best_estimator_
# # Evaluate the best model
# knn_pred = best_knn_model.predict(X_test)
#
# # Random Forests
# rf_model = RandomForestClassifier()
# # Initialize GridSearchCV
# grid_search = GridSearchCV(rf_model, param_grid_random_forest, cv=5, scoring='accuracy', n_jobs=-1)
# # Fit the grid search to the data
# grid_search.fit(X_train, y_train)
# # Get the best parameters
# best_params = grid_search.best_params_
# # Use the best model
# best_rf_model = grid_search.best_estimator_
# # Evaluate the best model
# rf_pred = best_rf_model.predict(X_test)

# TODO Try GridSearchCV for all of them


# Function to evaluate model performance

# Evaluate the performance of models
models = {
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'KNN': KNeighborsClassifier(),
    'Neural Network': MLPClassifier(max_iter=1000, random_state=42, solver='adam', learning_rate='adaptive', tol=1e-6, alpha=0.01, learning_rate_init=0.01, hidden_layer_sizes=(100,))
}

# Train and evaluate each model
for model_name, model in models.items():
    print(f"Training {model_name}...")
    model.fit(X_train, y_train)
    print(f"Evaluating {model_name}...")
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Print results
    print(f"Performance of {model_name}:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\n")

# Write to CSV file
#df_encoded.to_csv('data.csv', index=False)

correlation_matrix = df_encoded.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix')
#plt.show()
