import numpy as np
import pandas as pd

"Series are 1 dimensinal array that can hold any data"

array = np.array([1, 2, 3, 4])
series = pd.Series(array, index=["A", "B", "C", "D"])



"""
iloc - for integer position
loc - for str position
"""

dict_data = {"first day": 1400, "second day": 1200, "third day": 1200}
series = pd.Series(dict_data)
series.loc[series > 1200] -= (series - 1200)
# print(series)



"""
DataFrames are tabular data structure with columns, rows (2 dimensinal)
"""


data_dict = {
    "name": ["sponge bob", "patrick", "squidward"],
    "ages" : [30, 35, 40]    
}

df = pd.DataFrame(data=data_dict, index=["employee 1", "employee 2", "employee 3"])



# print(df.loc["employee 1"])
# print(df.iloc[1])


"add a new column"
df["job"] = ["cook", "N/A", "cashier"]
# print(df)


new_row = pd.DataFrame([{"name": "sandy", "ages": 30, "job": "engineer"}], index=["employee 4"])
df = pd.concat([df, new_row])
# print(df)



"""
importing is about to import a data from file to our pandas dataframe
"""

df_csv = pd.read_csv("data.csv")
df_json = pd.read_json("data.json")



"""
selection

"""

#selection by column

df = pd.read_csv("data.csv")
print(df["name"].to_string())



new_df = pd.DataFrame(
    {
        "name": ["beka", "sandy"],
        "age": [18, 18],
        "job" : ["backend", "frontend"]
    },
    index=["elployee1", "eployee2"]
    
)




new_column = pd.DataFrame(
    {
        "name": "ryan",
        "age": 18,
        "job": "flutter",
        "celery": 1000
    },
    index=["eployee4"]
)

new_df["celery"] = [1000, 1000]


new_df = pd.concat([new_df, new_column])
print(new_df)



new_series = pd.Series({"first day": 1400, "second day": 1200, "third day": 1200})
new_series[new_series > 1200] = series - 1000
print(new_series)