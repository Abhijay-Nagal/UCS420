import pandas as pd
import os


# ============================================================
# UCS420 - Cognitive Computing
# Assignment-3: Pandas
# ============================================================


# Get the folder where this Python file is located
folder_path = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# Q1. Create a dataset as given in the table
# ============================================================

data = {
    "Tid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Refund": [
        "Yes", "No", "No", "Yes", "No",
        "No", "Yes", "No", "No", "No"
    ],
    "Marital Status": [
        "Single", "Married", "Single", "Married", "Divorced",
        "Married", "Divorced", "Single", "Married", "Single"
    ],
    "Taxable Income": [
        "125K", "100K", "70K", "120K", "95K",
        "60K", "220K", "85K", "75K", "90K"
    ],
    "Cheat": [
        "No", "No", "No", "No", "Yes",
        "No", "No", "Yes", "No", "Yes"
    ]
}

df = pd.DataFrame(data)

print("\n================ Q1 ================")
print("Dataset created in Q1:")
print(df)


# ============================================================
# Q2. Locate row 0, 4, 7 and 8 using DataFrame
# ============================================================

print("\n================ Q2 ================")
print("Rows with index 0, 4, 7 and 8:")

q2_result = df.loc[[0, 4, 7, 8]]

print(q2_result)


# ============================================================
# Q3. Navigate the DataFrame
# ============================================================

print("\n================ Q3 ================")


# Q3(1). Select row from index 3 to 7

print("\n1. Rows from index 3 to 7:")

q3_1 = df.loc[3:7]

print(q3_1)


# Q3(2). Select row from index 4 to 8,
# and column 2 to 4

print("\n2. Rows from index 4 to 8 and columns 2 to 4:")

q3_2 = df.iloc[4:9, 2:5]

print(q3_2)


# Q3(3). Select all rows with column index 1 to 3
# Include index 3 during selection

print("\n3. All rows with column index 1 to 3:")

q3_3 = df.iloc[:, 1:4]

print(q3_3)


# ============================================================
# Q4. Read a CSV file and display its first five rows
# ============================================================

iris_file = os.path.join(folder_path, "iris.csv")

iris_df = pd.read_csv(iris_file)

print("\n================ Q4 ================")
print("First five rows of Iris dataset:")

print(iris_df.head())


# ============================================================
# Q5. Delete row 4 and column 3
# ============================================================

# Delete row with index 4
q5_df = iris_df.drop(index=4)

# Delete column with index 3
q5_df = q5_df.drop(q5_df.columns[3], axis=1)

print("\n================ Q5 ================")
print("After deleting row 4 and column 3:")

print(q5_df)


# ============================================================
# Q6. Create and analyze employees.csv
# ============================================================

employees_file = os.path.join(folder_path, "employees.csv")

employees = pd.read_csv(employees_file)


# ============================================================
# Q6(a). Shape of the DataFrame
# ============================================================

print("\n================ Q6(a) ================")

print("Shape of DataFrame:")

print(employees.shape)


# ============================================================
# Q6(b). Summary of the DataFrame
# ============================================================

print("\n================ Q6(b) ================")

print("Summary of DataFrame:")

employees.info()


# ============================================================
# Q6(c). Generate descriptive statistics
# ============================================================

print("\n================ Q6(c) ================")

print("Descriptive Statistics:")

print(employees.describe())


# ============================================================
# Q6(d). Display first 5 rows and last 3 rows
# ============================================================

print("\n================ Q6(d) ================")

print("First 5 rows:")

print(employees.head(5))

print("\nLast 3 rows:")

print(employees.tail(3))


# ============================================================
# Q6(e). Calculate statistics
# ============================================================

print("\n================ Q6(e) ================")


# i. Average salary of employees

average_salary = employees["Salary"].mean()

print("i. Average Salary:", average_salary)


# ii. Total bonus paid to all employees

total_bonus = employees["Bonus"].sum()

print("ii. Total Bonus:", total_bonus)


# iii. Youngest employee's age

youngest_age = employees["Age"].min()

print("iii. Youngest Employee's Age:", youngest_age)


# iv. Highest performance rating

highest_rating = employees["Rating"].max()

print("iv. Highest Performance Rating:", highest_rating)


# ============================================================
# Q6(f). Sort DataFrame by Salary in descending order
# ============================================================

print("\n================ Q6(f) ================")

sorted_employees = employees.sort_values(
    by="Salary",
    ascending=False
)

print("Employees sorted by Salary in descending order:")

print(sorted_employees)


# ============================================================
# Q6(g). Categorize employees based on performance rating
# ============================================================

print("\n================ Q6(g) ================")


def performance_category(rating):

    if rating >= 4.5:
        return "Excellent"

    elif rating >= 4.0:
        return "Good"

    else:
        return "Average"


employees["Performance"] = employees["Rating"].apply(
    performance_category
)

print("DataFrame with Performance Category:")

print(employees)


# ============================================================
# Q6(h). Identify missing values
# ============================================================

print("\n================ Q6(h) ================")

print("Missing values in each column:")

print(employees.isnull().sum())


# ============================================================
# Q6(i). Rename Employee_ID column to ID
# ============================================================

print("\n================ Q6(i) ================")

employees.rename(
    columns={"Employee_ID": "ID"},
    inplace=True
)

print("DataFrame after renaming Employee_ID to ID:")

print(employees)


# ============================================================
# Q6(j). Find all employees who:
# ============================================================

print("\n================ Q6(j) ================")


# i. Have more than 5 years of experience

employees_more_than_5_years = employees[
    employees["Years_of_Experience"] > 5
]

print("i. Employees with more than 5 years of experience:")

print(employees_more_than_5_years)


# ii. Belong to the IT department

it_employees = employees[
    employees["Department"] == "IT"
]

print("\nii. Employees belonging to IT department:")

print(it_employees)


# ============================================================
# Q6(k). Add a new column Tax
# ============================================================

print("\n================ Q6(k) ================")

# Tax is 10% of Salary

employees["Tax"] = employees["Salary"] * 0.10

print("DataFrame after adding Tax column:")

print(employees)


# ============================================================
# Q6(l). Save the modified DataFrame to a new CSV file
# ============================================================

print("\n================ Q6(l) ================")

modified_file = os.path.join(
    folder_path,
    "employees_modified.csv"
)

employees.to_csv(
    modified_file,
    index=False
)

print("Modified DataFrame saved as employees_modified.csv")
print("File location:", modified_file)