import pandas as pd
from sklearn.model_selection import train_test_split

##Load cleaned data 
def load_csv(file_path):
    try:
        cleaned_data = pd.read_csv(file_path)
        print = "Data Loaded from {file_path}"
        return cleaned_data
    
    #Exception provided for file-load error
    except Exception as e:
        print(f"Error Loading CSV file: {e}")
        return None
    
# Function to split data 
def split_data(cleaned_data):
    training_data, testing_data = train_test_split(cleaned_data, test_size = 0.2, random_state = 42)
    training_data.to_csv('VSC Projects/Working Projects/In-Progress/SeniorProjects/NamUS_training_data.csv', index=False)
    testing_data.to_csv('C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/NamUS_testing_data.csv', index=False)


def main():
    file_path = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Cleaned_Data_NamUS.csv'
    #Run Function to laad clean NameUS data
    data = load_csv(file_path)

    #If data is found, split into testing and training files
    if data is not None:
        split_data(data)

#Run main function
if __name__ == "__main__":
    main()


