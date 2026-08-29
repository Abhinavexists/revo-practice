import numpy as np
import pandas as pd

data = [1,2,3,4,5]
data_dict = {
    'a': 1,
    'b': 2,
    'c': 3,
}
index = ['a','b','c','d','e']
# dataframe
df_data = {
    'Name': ['abhi', 'abhi1', 'abhi2'],
    'Age': [21, 22, 23],
    'City': ['Delhi', 'Bengaluru', 'Nainital']
}

series = pd.Series(data) # 1D array
print("Series \n", series)

series_dict = pd.Series(data_dict) # 1D array of dict element
print("Series Dict \n", series_dict)

data_index_pair = pd.Series(data=data, index=index) # if want to pair data with specific set of index
print("Data Index Pair \n", data_index_pair)

make_df = pd.DataFrame(df_data)
print("Make Dataframe \n",make_df)
print(type(make_df))

np_array_of_df = np.array(make_df) # can change to array by using np
print(np_array_of_df)

df_sales = pd.read_csv('sales_data.csv')
print(df_sales.head(5)) # first 5 records
print(df_sales.tail(5)) # last 5 records

print(df_data['Name'])
print(type(df_data['Name']))

print(make_df.loc[0]) # going with row index
print(make_df.at[2, 'City']) # access single element
print(make_df.iat[2,2]) # access single element using integer only

make_df_copy = make_df.copy() # shallow copy
make_df_copy['Salary'] = [50000, 60000, 70000]
print(make_df_copy)
print(type(make_df_copy))
# make_df_copy.drop('Salary', axis=1, inplace=True)

# increment or decrement in a column
make_df_copy['Age']  = make_df_copy['Age'] + 1
print(make_df_copy)

print(make_df.dtypes) # all dtype info
print(make_df.describe()) # describe the dataframe
