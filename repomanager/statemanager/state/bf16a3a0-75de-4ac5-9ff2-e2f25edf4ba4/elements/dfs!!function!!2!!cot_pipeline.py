def cot_pipeline():
    data, filename = open_data_json()
    create_cot(data)
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)
