with open('data.json', 'r') as json_file:  # do not write as binary
    data = json.load(json_file)

print(data)