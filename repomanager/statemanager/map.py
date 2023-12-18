import click
import os
import shutil
import json

repo_map = json.load(open('./repo_map.json'))

ignore = []
# pring working directory
print(os.getcwd())
# go to the root directory
os.chdir('../../')
print(os.getcwd())
# open gitignore from the root directory
with open('.gitignore', 'r') as f:
    ignore_ = f.readlines()
for i in ignore_:
    # if the line isn't a comment or a space or a newline
    if i[0] != '#' and i[0] != '\n' and i[0] != ' ':
        # strip the newline
        ignore.append(i.strip())
ignore.append('.json')
ignore.append('.txt')
os.chdir('repomanager/statemanager')

@click.command()
@click.argument('repo_name')
def flatten_repo(repo_name):
    if repo_name in repo_map.keys():
        repo_id = repo_map[f'{repo_name}']
        flattened_folder = os.path.join('data/flattened', repo_id)
        os.makedirs(flattened_folder, exist_ok=True)
        path_file = os.path.join(flattened_folder, 'path.txt')
        directory_file = os.path.join(flattened_folder, 'directory.txt')
        with open(directory_file, 'w') as f_:
            with open(path_file, 'w') as f:
                # create a folder titled files
                files_folder = os.path.join(flattened_folder, 'files')
                os.makedirs(files_folder, exist_ok=True)
                for root, dirs, files in os.walk(os.path.join('data', repo_id)):
                    for file in files:
                        filename = os.path.join(root, file)
                        cont = False
                        for i in ignore:
                            if i in filename:
                                cont = True
                                break
                        if cont:
                            continue
                        directory = filename.split(f'{repo_id}')[1]
                        f_.write(directory + '\n')
                        f.write(os.path.join(root, file) + '\n')
                        # for each file, copy its contents, and save it into a .txt file with the name os.path.join(root, file)
                        # in the files folder
                        list_of_files_that_failed = []
                        with open(filename, 'r') as f2:
                            try:
                                content = f2.read()
                                # replace the / in the path with _
                                file = os.path.join(root, file).replace('/', '_')
                                with open(os.path.join(files_folder, file), 'w') as f3:
                                    f3.write(content)
                            except:
                                continue
    else:
        click.echo(f"Repo {repo_name} is not cloned.")

if __name__ == '__main__':
    flatten_repo()