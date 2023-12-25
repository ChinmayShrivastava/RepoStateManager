def open_files(folder='data'):
    fol = input('Enter folder name: ')
    if fol:
        folder = fol
    files = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(f'{folder}' + filename, 'r') as f:
                files.append(f.read())
    return files
