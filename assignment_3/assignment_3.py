import pandas as pd
import os

folder = os.path.dirname(os.path.abspath(__file__))

# Q1
data = {
    "Tid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Refund": ["Yes", "No", "No", "Yes", "No", "No", "Yes", "No", "No", "No"],
    "Marital Status": ["Single", "Married", "Single", "Married", "Divorced", "Married", "Divorced", "Single", "Married", "Single"],
    "Taxable Income": ["125K", "100K", "70K", "120K", "95K", "60K", "220K", "85K", "75K", "90K"],
    "Cheat": ["No", "No", "No", "No", "Yes", "No", "No", "Yes", "No", "Yes"]
}

df = pd.DataFrame(data)
print(df)

# Q2
print(df.loc[[0, 4, 7, 8]])

# Q3
print(df.loc[3:7])
print(df.iloc[4:9, 2:5])
print(df.iloc[:, 1:4])

# Q4
iris_file = os.path.join(folder, "iris.csv")
iris_df = pd.read_csv(iris_file)
print(iris_df.head())

# Q5
q5_df = iris_df.drop(index=4)
q5_df = q5_df.drop(q5_df.columns[3], axis=1)
print(q5_df)

# Q6
employees_file = os.path.join(folder, "employees.csv")
employees = pd.read_csv(employees_file)

# a
print(employees.shape)

# b
employees.info()

# c
print(employees.describe())

# d
print(employees.head(5))
print(employees.tail(3))

# e
print("Average Salary:", employees["Salary"].mean())
print("Total Bonus:", employees["Bonus"].sum())
print("Youngest Employee Age:", employees["Age"].min())
print("Highest Rating:", employees["Rating"].max())

# f
sorted_employees = employees.sort_values(by="Salary", ascending=False)
print(sorted_employees)

# g
def performance_category(rating):
    if rating >= 4.5:
        return "Excellent"
    elif rating >= 4.0:
        return "Good"
    else:
        return "Average"

employees["Performance"] = employees["Rating"].apply(performance_category)
print(employees)

# h
print(employees.isnull().sum())

# i
employees.rename(columns={"Employee_ID": "ID"}, inplace=True)
print(employees)

# j
print(employees[employees["Years_of_Experience"] > 5])
print(employees[employees["Department"] == "IT"])

# k
employees["Tax"] = employees["Salary"] * 0.10
print(employees)

# l
modified_file = os.path.join(folder, "employees_modified.csv")
employees.to_csv(modified_file, index=False)