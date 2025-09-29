import pandas as pd
import numpy as np
from rapidfuzz import process

# Disappearance age, disappearance location (state, city, county), sex, ethnicity
keep_columns = ['Age From', 'City', 'County', 'State', 'Biological Sex', 'Race / Ethnicity']

# Renaming Dictionary for Columns 
rename_dict = {
    'Age From': 'Age',
    'City': 'City',
    'County': 'County',
    'State': 'State',
    'Biological Sex': 'Sex',
    'Race / Ethnicity': 'Race / Ethnicity'
}

# Last Data Update: 2/22/2025 
# Load data
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}. Shape: {data.shape}")
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return None

# Load reference database for city, state and county 
def load_location_data(city_file, county_file, state_file):
    try:
        cities = pd.read_csv(city_file)
        counties = pd.read_csv(county_file)
        states = pd.read_csv(state_file)
        valid_cities = cities['Cities'].dropna().unique()
        valid_counties = counties['County'].dropna().unique()
        valid_states = states['State'].dropna().unique()
        print("Location data loaded successfully.")
        return valid_cities, valid_counties, valid_states
    
    except Exception as e:
        print(f"Error loading location data: {e}")
    return None, None, None

# Fuzzy Matching Function
def valid_location_input(value, valid_values, threshold=75):
    if isinstance(value, str):
        value = value.lower()  
        match = process.extractOne(value, valid_values, score_cutoff=threshold)
        if match:
            return match[0]
    return None
   
def clean_data(data, keep_columns, valid_cities, valid_counties, valid_states):
    output_file_path = r'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Cleaned_Data_NamUS.csv'
    
    if data is not None:
        try:
            print("Starting data cleaning...")
            
            # Remove rows with missing values
            cleaned_data = data.dropna()

            # Keep only the required columns
            cleaned_data = cleaned_data[keep_columns]
            
            # Remove rows where 'Age' is negative
            if 'Age' in cleaned_data.columns:
                cleaned_data = cleaned_data[cleaned_data['Age'] >= 0]
                
            # Rename Columns 
            cleaned_data = cleaned_data.rename(columns=rename_dict)

            # Correct City, County, and State names using fuzzy matching
            print(f"Processing City column...")
            cleaned_data['City'] = cleaned_data['City'].apply(lambda x: valid_location_input(x, valid_cities))
            print(f"Processing County column...")
            cleaned_data['County'] = cleaned_data['County'].apply(lambda x: valid_location_input(x, valid_counties))
            print(f"Processing State column...")
            cleaned_data['State'] = cleaned_data['State'].apply(lambda x: valid_location_input(x, valid_states))

            # Remove rows with invalid location data
            cleaned_data = cleaned_data.dropna(subset=['City', 'County', 'State'])

            # Save cleaned data 
            cleaned_data.to_csv(output_file_path, index=False)
            print(f"Cleaned data saved to '{output_file_path}'")
        
        except Exception as e:
            print(f"Error during data cleaning: {e}")
            return None

        return cleaned_data
    else:
        return None

def main():
    file_path = r'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Uncleaned_Data_NamUS.csv'
    city_file = r'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Reference-Data/cities.csv'
    county_file = r'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Reference-Data/counties.csv'
    state_file = r'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Reference-Data/states.csv'
   
    # Load the dataset and location reference files
    data = load_csv(file_path)
    valid_cities, valid_counties, valid_states = load_location_data(city_file, county_file, state_file)
    
    # Run cleaning
    try:
        clean_data(data, keep_columns, valid_cities, valid_counties, valid_states)
    except Exception as e:
        print(f"Unhandled exception during data cleaning process: {e}")

if __name__ == "__main__":
    main()
