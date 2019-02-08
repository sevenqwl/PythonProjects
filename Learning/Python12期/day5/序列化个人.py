import pickle,json

# pickle

# with open("user_acc.txt", "rb") as f:
#     data_from_atm = pickle.loads(f.read())
#     print(data_from_atm)
#
# with open("user_acc.txt", "rb") as f:
#     data_from_atm = pickle.load(f)
#     print(data_from_atm)

# json

with open("user_acc.txt", "r") as f:
    data_from_atm = json.loads(f.read())
    print(data_from_atm)

with open("user_acc.txt", "r") as f:
    data_from_atm = json.load(f)
    print(data_from_atm)
