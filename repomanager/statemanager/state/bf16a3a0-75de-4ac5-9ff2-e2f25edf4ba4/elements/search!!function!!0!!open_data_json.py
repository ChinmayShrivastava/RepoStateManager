def open_data_json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    return data
