import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import silhouette_score
from kneed import KneeLocator 
from matplotlib.lines import Line2D

# Set CPU limitation 
os.environ["LOKY_MAX_CPU_COUNT"] = "6"  
# Set style 
plt.style.use('seaborn-v0_8-darkgrid')

#Loading Testing and Training data 
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {len(data)} records from {file_path}")
        return data
    
    except Exception as e:
        print(f"Error Loading Data: {e}")
        return None
# Assign cluster profiles, define demographics and geographics
class ClusterAnalyzer:
    def __init__(self, n_clusters='auto', max_k=10):
        self.n_clusters = n_clusters
        self.max_k = max_k
        self.pipeline = None
        self.cluster_profiles = {}
        self.demographic_columns = [
            'remainder__Age', 'remainder__Sex', 
            'remainder__Race / Ethnicity'
        ]
        self.location_columns = [
            'remainder__State', 'remainder__City', 
            'remainder__County'
        ]
     # Determine clusters (Silhoutette Anaylsis  & Elbow Method)   
    def find_optimal_clusters(self, X):
        inertias = []
        silhouette_scores = []
        k_range = range(2, self.max_k + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, labels))
        
        # Determine elbow automatically
        elbow = KneeLocator(
            k_range, inertias, curve='convex', direction='decreasing'
        ).elbow
        
        # Optimal k ->  Elbow point or Max Silhouette Score
        optimal_k = elbow if elbow is not None else np.argmax(silhouette_scores) + 2
        
        # Plotting of clusters 3
        # Elbow Method Clusters
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(k_range, inertias, marker='o')
        plt.axvline(x=optimal_k, color='r', linestyle='--')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title('Elbow Method')
        
        # Silhouette Score Method Clusters
        plt.subplot(1, 2, 2)
        plt.plot(k_range, silhouette_scores, marker='o')
        plt.axvline(x=optimal_k, color='r', linestyle='--')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Analysis')
        plt.tight_layout()
        plt.show()
        
        return optimal_k
    
    def fit(self, X_train):
        self.features = self.demographic_columns + self.location_columns
        X_scaled = StandardScaler().fit_transform(X_train[self.features])
        
        # Dynamic cluster selection 
        if self.n_clusters == 'auto':
            self.n_clusters = self.find_optimal_clusters(X_scaled)
        
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('cluster', KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10))
        ])
        
        self.pipeline.fit(X_train[self.features])
        self.create_cluster_profiles(X_train)
        return self
    
    def transform(self, X):
        clusters = self.pipeline.predict(X[self.features])
        return X.assign(Cluster=clusters)
    
    def create_cluster_profiles(self, X_train):
        train_clusters = self.pipeline.predict(X_train[self.features])
        
        for c in range(self.n_clusters):
            cluster_data = X_train[train_clusters == c]
            profile = {
                'size': len(cluster_data),
                'avg_age': cluster_data['remainder__Age'].mean(),
                'common_sex': cluster_data['remainder__Sex'].mode()[0],
                'common_race': cluster_data['remainder__Race / Ethnicity'].mode()[0],
                'common_state': cluster_data['remainder__State'].mode()[0],
                'common_city': cluster_data['remainder__City'].mode()[0]
            }
            self.cluster_profiles[c] = profile

    def plot_clusters(self, X_train, X_test=None):
        """PCA visualization with test data support"""
        pca = PCA(n_components=2)
        X_train_pca = pca.fit_transform(
            self.pipeline.named_steps['scaler'].transform(X_train[self.features])
        )
        
        plt.figure(figsize=(12, 8))
        
        # Define custom color palette
        custom_palette = ["#031926","#468189", "#77ACA2","#A3C9A8","#F4E9CD","#5B6A82","#FFFFFF","#F8F9FA","#FF6B35"]
        
        # Plot training data
        train_df = pd.DataFrame(X_train_pca, columns=['PCA1', 'PCA2'])
        train_df['Cluster'] = self.pipeline.predict(X_train[self.features])
        train_plot = sns.scatterplot(
            data=train_df, 
            x='PCA1', 
            y='PCA2', 
            hue='Cluster',
            palette=custom_palette[:self.n_clusters],
            s=100,
            marker='o'
        )
        plt.title('Demographic-Location Patterns in Missing Persons Data')
        plt.xlabel('PCA1: Age & Location Variation')
        plt.ylabel('PCA2: Gender & Ethnicity Variation')
        
        # Plot test data
        if X_test is not None:
            X_test_pca = pca.transform(
                self.pipeline.named_steps['scaler'].transform(X_test[self.features])
            )
            test_df = pd.DataFrame(X_test_pca, columns=['PCA1', 'PCA2'])
            test_df['Cluster'] = self.pipeline.predict(X_test[self.features])
            test_plot = sns.scatterplot(
                data=test_df,
                x='PCA1',
                y='PCA2',
                hue='Cluster',
                palette=custom_palette[:self.n_clusters],
                s=100,
                marker='X'
            )
        
        # Add centroids
        centroids = pca.transform(
            self.pipeline.named_steps['cluster'].cluster_centers_
        )
        centroid_plot = plt.scatter(
            centroids[:, 0], 
            centroids[:, 1], 
            s=200, 
            c='#E35336',
            marker='*', 
            edgecolor='black'
        )
        # Define Legend 
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Training Data',
                markerfacecolor='grey', markersize=10),
            Line2D([0], [0], marker='X', color='w', label='Test Data',
                markerfacecolor='grey', markersize=10),
            Line2D([0], [0], marker='*', color='#E35336', label='Centroids',
                markersize=15, markeredgecolor='black'),
            *[Line2D([0], [0], marker='o', color='w', 
                    label=f'Cluster {i}: {self.cluster_profiles[i]["size"]} cases',
                    markerfacecolor=custom_palette[i], markersize=10) 
            for i in range(self.n_clusters)]
        ]
        # Legend Display
        plt.legend(
        handles=legend_elements, 
        bbox_to_anchor=(1.05, 1), 
        loc='upper left',
     title=f'Key (Total Clusters: {self.n_clusters})'
        )
        plt.title(f'Cluster Distribution (k={self.n_clusters}): Training vs Test Data')
        plt.tight_layout()
        plt.savefig('C:/Users/pshaf/Documents/GitHub/Working-Projects/In-Progress/SeniorProjects/Visuals/Clusters.png')
        plt.show()

    def print_cluster_profiles(self):
        print("\nCluster Profiles:")
        for c, profile in self.cluster_profiles.items():
            print(f"\nCluster {c}:")
            print(f"Size: {profile['size']} cases")
            print(f"Average Age: {profile['avg_age']:.1f} years")
            print(f"Most Common Gender: {profile['common_sex']}")
            print(f"Dominant Race/Ethnicity: {profile['common_race']}")
            print(f"Most Frequent Location: {profile['common_city']}, {profile['common_state']}")

def main():
    train_path = 'In-Progress/SeniorProjects/Data-Management/Encoded-Data/Encoded_NamUS_training_data.csv'
    test_path = 'In-Progress/SeniorProjects/Data-Management/Encoded-Data/Encoded_NamUS_testing_data.csv'
    
    train_data = load_data(train_path)
    test_data = load_data(test_path)
    
    if train_data is not None and test_data is not None:
        # Dynamic clustering 
        analyzer = ClusterAnalyzer(n_clusters='auto', max_k=10).fit(train_data)
        
        train_clustered = analyzer.transform(train_data)
        test_clustered = analyzer.transform(test_data)
        
        analyzer.plot_clusters(train_data, test_data)
        analyzer.print_cluster_profiles()

    train_clustered.to_csv('clustered_data.csv', index=False)

if __name__ == "__main__":
    main()