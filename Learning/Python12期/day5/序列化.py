import pickle,json

info = {
    "alex":"123",
    "jack":"4444"
}


# pickle
#
# with open("user_acc.txt", "wb") as f:
#     f.write(pickle.dumps(info))

# with open("user_acc.txt", "wb") as f:
#     pickle.dump(info, f)


# json

# with open("user_acc.txt", "w") as f:
#     json.dumps(info)
#
with open("user_acc.txt", "w") as f:
    json.dump(info, f)