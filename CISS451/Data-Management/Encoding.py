import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Function to load the data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data Loaded from {file_path}")
        return data
    except Exception as e:
        print(f"Error Loading CSV file: {e}")
        return None

# Encode data
def encode_data(train_file, test_file):
    # Load training and testing data
    train_data = load_data(train_file)
    test_data = load_data(test_file)

    if train_data is not None and test_data is not None:
        # Combine training and testing data 
        combined_data = pd.concat([train_data, test_data], axis=0)

        # Initialize LabelEncoder 
        label_encoder = LabelEncoder()
        
        # Dictionary to store label encoding mappings
        label_encodings = {}

        # Apply Label Encoding  
        for column in combined_data.select_dtypes(include=['object']).columns:
            unique_values = combined_data[column].unique()
            category_mapping = {val: idx for idx, val in enumerate(unique_values)}

            # Save the mapping for each column
            label_encodings[column] = category_mapping

            # Map categories to both train and test datasets
            train_data[column] = train_data[column].map(category_mapping)
            test_data[column] = test_data[column].map(category_mapping).fillna(-1)

        # Print the label encoding mappings
        print("Label Encoding Mappings:")
        for column, encoding in label_encodings.items():
            print(f"{column}: {encoding}")

        # Apply One-Hot Encoding 
        categorical_columns = train_data.select_dtypes(include=['object']).columns.tolist()

        one_hot_encoder = ColumnTransformer(
            transformers=[('cat', OneHotEncoder(drop='first'), categorical_columns)],
            remainder='passthrough'  # Keep numeric columns
        )

        # Fit and transform the training data
        train_data_encoded = one_hot_encoder.fit_transform(train_data)
        test_data_encoded = one_hot_encoder.transform(test_data)

        # Get the feature names from the OneHotEncoder
        one_hot_columns = one_hot_encoder.get_feature_names_out()

        # Print the one-hot encoding column names
        print("\nOne-Hot Encoding Mappings:")
        print(f"One-Hot Encoded Columns: {one_hot_columns}")

        # Convert to DataFrame
        train_data_encoded_df = pd.DataFrame(train_data_encoded, columns=one_hot_columns)
        test_data_encoded_df = pd.DataFrame(test_data_encoded, columns=one_hot_columns)

        # Return the encoded data
        return train_data_encoded_df, test_data_encoded_df

    return None, None

# Save the encoded data to CSV
def encoded_data(train_data_encoded, test_data_encoded, train_output_file, test_output_file):
    if train_data_encoded is not None and test_data_encoded is not None:
        train_data_encoded.to_csv(train_output_file, index=False)
        test_data_encoded.to_csv(test_output_file, index=False)
        print(f"Encoded data saved to {train_output_file} and {test_output_file}")
    else:
        print("Error in saving encoded data.")


# Run the encoding process W/Main
def main():
    train_file_path = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/NamUS_training_data.csv'
    test_file_path = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/NamUS_testing_data.csv'
    
    # Output paths
    train_output_file = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Encoded-Data/Encoded_NamUS_training_data.csv'
    test_output_file = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Encoded-Data/Encoded_NamUS_testing_data.csv'

    # Encoding
    train_data_encoded, test_data_encoded = encode_data(train_file_path, test_file_path)
    
    # Save to CSV
    encoded_data(train_data_encoded, test_data_encoded, train_output_file, test_output_file)

if __name__ == '__main__':
    main()
