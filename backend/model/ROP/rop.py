import pandas as pd
import numpy as np

df =pd.read_csv("project.csv" , encoding = "latin1")

df.head()

df.shape

np.random.seed(42)  # ADD QUANTITY
df['quantity'] = np.random.randint(250 , 400, size=len(df))

df.head()

np.random.seed(42)  # ADD QUANTITY
df['TOTAL_DAYS'] = np.random.randint(20 , 45, size=len(df))

df.head()

df['Demand_rate']= (df['quantity']/df["TOTAL_DAYS"])

df.head()

# service level
np.random.seed(42)  # ADD QUANTITY
df['SERVICE_LEVEL'] = np.random.randint(85 , 95, size=len(df))
df.head()

# CALCULATING THE LEAD TIME
# time require to receivce a money


# Calculate the mean and standard deviation of the 'Service_level' column
mean_service_level = df['SERVICE_LEVEL'].mean()
std_dev_service_level = df['SERVICE_LEVEL'].std()

# Calculate the Z-scores for the 'Service_level' column
df['Service_level_Z_score'] = ((df['SERVICE_LEVEL'] - mean_service_level) / std_dev_service_level)

df.head()

df['Demand_rate'] = df['Demand_rate'].round()

df.head()

#Ntime reqired to receive ineventory
# service level
np.random.seed(42)  # ADD QUANTITY
df['DAYS_REQ_TO_RECIVE_ORDER'] = np.random.randint(15  , 25, size=len(df))  # LEAD TIME
df.head()

# Calculate the standard deviation of the 'Demand_rate' column
std_dev_demand_rate = df['Demand_rate'].std()

# Calculate the Safety_stock
df['Safety_stock'] = std_dev_demand_rate * df['Service_level_Z_score'] * np.sqrt(df['DAYS_REQ_TO_RECIVE_ORDER'])
df.head()



df.head()

df['Safety_stock'] = np.abs(df['Safety_stock'])

df.head()



df.head()

df['Safety_stock'] = df['Safety_stock'].astype(int)

df.head()

df['ROP'] = (df['Demand_rate']* df['DAYS_REQ_TO_RECIVE_ORDER'])+ df['Safety_stock']

df.head()

#

df.head()

columns_to_delete = [
    '_id', 'actual_price', 'average_rating', 'brand', 'category',
    'crawled_at', 'description', 'discount', 'images', 'title', 'url',
    'sub_category', 'selling_price', 'out_of_stock', 'pid',
    'product_details', 'seller', 'Unnamed: 0'
]

# Delete the specified columns and create a new DataFrame
new_df = df.drop(columns=columns_to_delete)

new_df.head()

delete = ['SERVICE_LEVEL' , 'Service_level_Z_score', 'TOTAL_DAYS', 'TOTAL_DAYS']
final_table = new_df.drop(columns= delete)

final_table.head()

# Define features and target variable
X = df[['quantity', 'Demand_rate', 'DAYS_REQ_TO_RECIVE_ORDER', 'Safety_stock']]
y = df['ROP']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')

r2 = r2_score(y_test, y_pred)
print(r2)