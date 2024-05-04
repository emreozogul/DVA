import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def predict_target(X_test):
    # Define feature names
    feature_names = ['Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Roundness', 'Aspect_Ratio', 'Solidity', 'Convexity',
                     'Particle_Count']

    # Create a DataFrame for test data with feature names
    X_test_df = pd.DataFrame(X_test, columns=feature_names)

    # Scale test data using the same MinMaxScaler
    X_test_scaled = min_max_scaler.transform(X_test_df)

    # Make predictions
    y_pred = best_rf_model.predict(X_test_scaled)

    # Determine the target string based on the predicted index
    target_strings = {
        0: 'Healthy',
        1: 'Slightly Death',
        2: 'Extremely Death'
    }
    index = y_pred.argmax()
    return target_strings[index]

# Takes the folder path as input and returns the path to the latest CSV file in that folder.
def get_latest_csv_file():
    # Get a list of all files in the folder
    files = os.listdir(os.path.join(os.getcwd(), 'prework', 'data'))
    print(files)

    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    # Sort the CSV files based on their timestamps
    sorted_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join('prework', 'data', x)), reverse=True)

    if sorted_files:
        # Return the path to the latest CSV file
        return os.path.join('prework', 'data', sorted_files[0])
    else:
        return None


# Load the dataset
latest_csv_file = get_latest_csv_file()
if latest_csv_file:
    print("Latest CSV file: " + latest_csv_file)
    data = pd.read_csv(latest_csv_file)
else:
    print("No CSV files found in the folder.")

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

target_columns = ['Target_Healthy', 'Target_Slightly Death', 'Target_Extremely Death']
remaining_columns = [col for col in df_encoded.columns if col not in target_columns]
df_encoded = df_encoded[remaining_columns + target_columns]

num_cols = [col for col in df_encoded.columns if
            col not in ['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death']]

min_max_scaler = MinMaxScaler()
df_encoded[num_cols] = min_max_scaler.fit_transform(df_encoded[num_cols])

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

# Separate independent variables (X) and target variable (y)
X = df_encoded.drop(columns=['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death'])
y = df_encoded[['Target_Healthy', 'Target_Slightly Death', 'Target_Extremely Death']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the base estimator
base_estimator = RandomForestClassifier()

# Define the parameter grid for Random Forest
param_grid_rf = {
    'n_estimators': [200, 300, 400],
    'max_depth': [10, 20, 25],
    'min_samples_split': [5, 10, 12],
    'min_samples_leaf': [2, 4, 5]
}

# Perform Grid Search with Random Forest
grid_search_rf = GridSearchCV(base_estimator, param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1)
grid_search_rf.fit(X_train, y_train)

# Get the best Random Forest model
best_rf_model = grid_search_rf.best_estimator_

# Feature importance from RandomForestClassifier
feature_importance = best_rf_model.feature_importances_

# Perform cross-validation with the best Random Forest model
cv_scores = cross_val_score(best_rf_model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
average_cv_score = cv_scores.mean()

# Predict using the best Random Forest model
y_pred_rf = best_rf_model.predict(X_test)

# Calculate evaluation metrics for Random Forest
accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf, average='weighted')
recall_rf = recall_score(y_test, y_pred_rf, average='weighted')
f1_rf = f1_score(y_test, y_pred_rf, average='weighted')

# Print the evaluation metrics for Random Forest
print("Performance of Random Forest:")
print(f"Cross-Validation Accuracy: {average_cv_score:.4f}")
print(f"Test Accuracy: {accuracy_rf:.4f}")
print(f"Precision: {precision_rf:.4f}")
print(f"Recall: {recall_rf:.4f}")
print(f"F1 Score: {f1_rf:.4f}")