import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the training and testing data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data Loaded from {file_path}")
        return data
    except Exception as e:
        print(f"Error Loading CSV file: {e}")
        return None
    
# Prepare data by separating features (X) and target (y)
def prepare_data(data, target_column):
    X = data.drop(columns=[target_column]) 
    y = data[target_column]  
    return X, y

# Random Forest Model 
def random_forest(X_train, y_train, X_test, y_test):
    #Initate Random Forest 
    rf_model = RandomForestClassifier(random_state=42)

    #Train Random Forest Model
    rf_model.fit(X_train, y_train)

    #Predictions
    y_pred_rf = rf_model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred_rf)
    print(f"Accuracy: {accuracy * 100:.2f}%")
        
    # Confusion matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_rf))
        
    # Classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred_rf))

def main():
    # File paths for the training and testing sets
    train_file_path = 'In-Progress\SeniorProjects\Data-Management\Encoded-Data\Encoded_NamUS_training_data.csv'
    test_file_path = 'In-Progress\SeniorProjects\Data-Management\Encoded-Data\Encoded_NamUS_testing_data.csv'
    
    # Load the training and testing data
    train_data = load_data(train_file_path)
    test_data = load_data(test_file_path)
    
    if train_data is not None and test_data is not None:
        target_column = 'remainder__Sex'

        # Prepare training and testing data
        X_train, y_train = prepare_data(train_data, target_column)
        X_test, y_test = prepare_data(test_data, target_column)

        # Run random forest
        random_forest(X_train, y_train, X_test, y_test)

# Run main function
if __name__ == "__main__":
    main()


