import pandas as pd
import numpy as np

df = pd.read_csv("project.csv" , encoding = "latin1")

df.head()

df.info()

# Step 2: Convert actual_price and selling_price to int data type
# Remove commas and convert, handling non-convertible values
df['actual_price'] = pd.to_numeric(df['actual_price'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
df['selling_price'] = pd.to_numeric(df['selling_price'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)


# Step 3: Verify the changes
print(df[['actual_price', 'selling_price']].dtypes)

df

df["selling_price"]=df["selling_price"]*6

df.head()

# Step 2: Remove "% off" from the discount column
df['description'] = df['description'].str.replace('% off', '')

# Step 3: Handle NaN values (if any)
df['description'] = df['description'].fillna('0')  # Replace NaN with '0'

# Step 4: Convert the discount column to integer
df['description'] = df['description'].astype(int)

# Step 5: Display the modified DataFrame
print(df)

df

# Step 2: Generate a column of random numbers for quantity (between 1 and 15)
np.random.seed(42)  # For reproducibility
df['quantity'] = np.random.randint(10, 20, size=len(df))

df.head()

np.random.seed(42)  # For reproducibility
df['marketing_price'] = np.random.randint(500, 700, size=len(df))

df.head()

df['initial_price']= (df['actual_price']*df['quantity'])

df.head()

np.random.seed(42)  # For reproducibility
df['raw_sell_price'] = np.random.randint(30000 , 70000, size=len(df))

df.head()

df['discounted_price'] = df['selling_price'] * (1 - df['description'] / 100)

df['final_selling_price']= df['raw_sell_price']-df['discounted_price']

df.head()# raw selling price is just ramdom entity betwwn  50000, 100000,
# final sell price is 	raw_sell_price-discounted_price
#initial price is actual price * quantity

df["profit"]= df['final_selling_price']-(df['initial_price']+df['marketing_price'])

df.head()

df["investment"]=  df['initial_price']+ df['marketing_price']
df.head()

df["ROI"]= (df["profit"] / df['investment'])*100

df.head()

columns=['url','initial_price','raw_sell_price','discounted_price','profit','investment','_id','crawled_at','brand','discount','images','pid','product_details','seller','sub_category','title' ,'actual_price', 'average_rating','brand','category','crawled_at','selling_price','discount','description','images','out_of_stock','pid','product_details','Unnamed: 0']

df_new=df.drop(columns,axis=1)

df_new

y=df_new['ROI']

X=df_new.drop('ROI',axis=1)

y

X



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_test

y_test

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)
#(final_selling_price, quantity, marketing_price).

len(predictions)

predictions

from sklearn.metrics import accuracy_score

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Display the results
print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

