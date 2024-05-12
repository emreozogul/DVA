import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

def predict_target(X_test ,best_rf_model, min_max_scaler):
    feature_names = ['Area_mm2', 'Perimeter_mm', 'Diameter_mm', 'Roundness', 'Aspect_Ratio', 'Solidity', 'Convexity',
                     'Particle_Count']
    
    X_test_df = pd.DataFrame(X_test, columns=feature_names)
    X_test_scaled = min_max_scaler.transform(X_test_df)
    y_pred = best_rf_model.predict(X_test_scaled)
    target_strings = {
        0: 'Healthy',
        1: 'Slightly Death',
        2: 'Extremely Death'
    }
    index = y_pred.argmax()
    return target_strings[index]

def get_latest_csv_file():
    files = os.listdir(os.path.join(os.getcwd(), 'prework', 'data'))
    print(files)
    
    csv_files = [file for file in files if file.endswith('.csv')]

    sorted_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join('prework', 'data', x)), reverse=True)

    if sorted_files:
        return os.path.join('prework', 'data', sorted_files[0])
    else:
        return None


def train_model():
    latest_csv_file = get_latest_csv_file()
    if latest_csv_file:
        data = pd.read_csv(latest_csv_file)
    else:
        print("No CSV files found in the folder.")
        return
    
    data = data.drop(columns=['Image_Name'], axis=1)
    
    categorical_column = ['Target']
    
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(data[categorical_column])
    
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_column))
    
    df_encoded = pd.concat([data, one_hot_df], axis=1)
    
    df_encoded = df_encoded.drop(categorical_column, axis=1)
    
    target_columns = ['Target_Healthy', 'Target_Slightly Death', 'Target_Extremely Death']
    remaining_columns = [col for col in df_encoded.columns if col not in target_columns]
    df_encoded = df_encoded[remaining_columns + target_columns]
    
    num_cols = [col for col in df_encoded.columns if col not in ['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death']]
    
    min_max_scaler = MinMaxScaler()
    df_encoded[num_cols] = min_max_scaler.fit_transform(df_encoded[num_cols])
    
    for column in df_encoded.columns[:-3]:
        Q1 = df_encoded[column].quantile(0.25)
        Q3 = df_encoded[column].quantile(0.75)
        
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_encoded[(df_encoded[column] < lower_bound) | (df_encoded[column] > upper_bound)]
        
        df_encoded = df_encoded.drop(outliers.index)
    
    X = df_encoded.drop(columns=['Target_Extremely Death', 'Target_Healthy', 'Target_Slightly Death'])
    y = df_encoded[['Target_Healthy', 'Target_Slightly Death', 'Target_Extremely Death']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    base_estimator = RandomForestClassifier()
    
    param_grid_rf = {
        'n_estimators': [200, 300, 400],
        'max_depth': [10, 20, 25],
        'min_samples_split': [5, 10, 12],
        'min_samples_leaf': [2, 4, 5]
    }
    
    grid_search_rf = GridSearchCV(base_estimator, param_grid_rf, cv=5, scoring='accuracy', n_jobs=-1)
    
    grid_search_rf.fit(X_train, y_train)
    
    best_rf_model = grid_search_rf.best_estimator_
        
    cv_scores = cross_val_score(best_rf_model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
    
    average_cv_score = cv_scores.mean()
    
    y_pred_rf = best_rf_model.predict(X_test)
    
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    
    precision_rf = precision_score(y_test, y_pred_rf, average='weighted')
    
    recall_rf = recall_score(y_test, y_pred_rf, average='weighted')
    
    f1_rf = f1_score(y_test, y_pred_rf, average='weighted')

    
    joblib.dump(best_rf_model, os.path.join('prework', 'models', 'best_rf_model.pkl'))
    joblib.dump(min_max_scaler, os.path.join('prework', 'models', 'min_max_scaler.pkl')) 
    json_data = {
        "accuracy": accuracy_rf,
        "precision": precision_rf,
    }
    return best_rf_model, min_max_scaler , json_data

def load_model():
    best_rf_model = joblib.load(os.path.join('prework', 'models', 'best_rf_model.pkl'))
    min_max_scaler = joblib.load(os.path.join('prework', 'models', 'min_max_scaler.pkl'))
    return best_rf_model, min_max_scaler
