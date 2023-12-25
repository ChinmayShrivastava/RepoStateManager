def open_data_json():
    # list all the .json files available in the data/ directory
    # ask the user to select one
    # open the selected file
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            print(filename)
    filename = input('Enter filename: ')
    if filename:
        with open(f'data/{filename}', 'r') as f:
            data = json.load(f)
    else:
        print("No filename entered. Using default data.json")
        filename = 'data.json'
        with open('data/data.json', 'r') as f:
            data = json.load(f)
    # with open('data/data.json', 'r') as f:
    #     data = json.load(f)
    return data, filename
