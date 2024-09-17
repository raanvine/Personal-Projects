import pandas as pand
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

path= 'Online Retail.xlsx'
dataset=pand.read_excel(path,sheet_name='Online Retail') #loads the excel file 
dataset.fillna(method='ffill', inplace=True) #cleans up data and replaces null entries 


scaler=StandardScaler()

dataset['InvoiceDate'] = pand.to_datetime(dataset['InvoiceDate']) #aggregates InvoiceDate to datetime 

# Aggregate data by customer
customer_data = dataset.groupby('CustomerID').agg({
    'Quantity': 'sum',
    'UnitPrice': 'mean',
    'InvoiceNo': 'count',
    'InvoiceDate': lambda x: (dataset['InvoiceDate'].max() - x.max()).days  # Recency
}).reset_index()

customer_data.columns = ['CustomerID', 'TotalQuantity', 'AverageUnitPrice', 'TransactionCount', 'Recency']

# Prepare features for clustering
features = customer_data[['TotalQuantity', 'AverageUnitPrice', 'TransactionCount', 'Recency']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(scaled_features)

# Evaluate clustering with silhouette score
silhouette_avg = silhouette_score(scaled_features, customer_data['Cluster'])
print(f'Silhouette Score: {silhouette_avg}')

# Display the first few rows of the clustered data
print(customer_data.head())

#plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=customer_data, x='TotalQuantity', y='AverageUnitPrice', hue='Cluster', palette='viridis')
plt.title('Clustering of Customers')
plt.xlabel('Total Quantity Purchased')
plt.ylabel('Average Unit Price')
plt.legend(title='Cluster')
plt.show()

if 'Country' not in dataset.columns:
    raise ValueError("The dataset does not contain a 'Country' column.")

# Aggregate quantity by country and product description
country_product_data = dataset.groupby(['Country', 'Description'])['Quantity'].sum().reset_index()

# Pivot the data for easier plotting
pivot_data = country_product_data.pivot_table(index='Description', columns='Country', values='Quantity', aggfunc='sum').fillna(0)

# Normalize the data for heatmap (optional, for better visualization)
normalized_data = pivot_data.div(pivot_data.sum(axis=0), axis=1) * 100

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(normalized_data, cmap='YlGnBu', annot=True, fmt='.1f', linewidths=.5)
plt.title('Product Purchase Frequency by Country')
plt.xlabel('Country')
plt.ylabel('Product Description')
plt.show()