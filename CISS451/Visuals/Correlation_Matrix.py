import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def labels(correlation_matrix):
    # Rename labels
    correlation_matrix.columns = [col.replace('remainder_', '').replace('_', '') for col in correlation_matrix.columns]
    correlation_matrix.index = [index.replace('remainder_', '').replace('_', '') for index in correlation_matrix.index]
    return correlation_matrix

def save_correlation_matrix(data, output_file='correlation_matrix.html'):
    # Select only numeric columns
    numeric_data = data.select_dtypes(include='number')
    
    # Compute correlation matrix
    correlation_matrix = numeric_data.corr()

    # Save the correlation matrix
    correlation_matrix_html = correlation_matrix.to_html()

    with open(output_file, 'w') as f:
        f.write(correlation_matrix_html)
    
    print(f"Correlation matrix saved as {output_file}")

def show_correlation_matrix(data, cmap):  
    numeric_data = data.select_dtypes(include='number')
    correlation_matrix = numeric_data.corr()
    correlation_matrix = labels(correlation_matrix)

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=cmap, square=True, linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    
    # Save the heatmap as an image
    plt.savefig("C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Visuals/correlation_matrix.png", dpi=300)  
    print("Correlation matrix heatmap saved as image.")
    
def main():
    file_path = 'C:/Users/pshaf/VSCProjects/Working-Projects/In-Progress/SeniorProjects/Data Management/Encoded-Data/Encoded_NamUS_training_data.csv'
    data = load_data(file_path)
    
    if data is not None:
        save_correlation_matrix(data) 
        
        custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", ['#031926','#468189','#77ACA2','#A3C9A8','#F4E9CD'])
        show_correlation_matrix(data, cmap=custom_cmap)

if __name__ == "__main__":
    main()
