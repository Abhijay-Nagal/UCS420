my_dict = {
    "name": "Abhijay Nagal",
    "roll_no": 1024170013,
    "branch": "COPC",
    "age": 20,
    "city": "Shimla"
}

my_dict["location"] = my_dict.pop("city")

my_dict["cgpa"] = 9.53

my_dict["age"] += 1

print(my_dict)

dict1 = my_dict.copy()
dict1.pop("branch")

print(dict1)

dict2 = my_dict.copy()
del dict2["branch"]

print(dict2)

for key, value in my_dict.items():
    print(key, "→", value)

if "email" in my_dict:
    print(my_dict["email"])
else:
    print("Email is not present in the dictionary.")

friend_dict = {
    "name": "Rahul Sharma",
    "roll_no": 87654321,
    "branch": "CSE",
    "age": 20,
    "city": "Delhi"
}

merged_dict = {**my_dict, **friend_dict}

print(merged_dict)

string_dict = {
    key: value
    for key, value in my_dict.items()
    if isinstance(value, str)
}

print(string_dict)