import sys
import os
# navigate two directories up
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
# print working directory
# mavigate to the top of working directory
os.chdir(dir)
print(os.getcwd())
from statemanager.standard.extract import markdown_parser, directory_file_iterator, ipynb_parser
from bs4 import BeautifulSoup
import random

if __name__ == '__main__':
    repo_id = '45526e5b-f544-4016-8381-f88f5ca095ea'
    files = directory_file_iterator(repo_id=repo_id, get_non_py_files=True)
    print(len(files))
    # randomize the fileorder
    files = random.sample(files, len(files))
    for file in files:
        if file.endswith('.ipynb'):
            # get the content of the file
            content = open(file).read()
            # parse the markdown
            parsed = ipynb_parser(content)
            # remove the html tags from each list element
            parsed = [BeautifulSoup(p, features="html.parser").get_text() for p in parsed]
        elif file.endswith('.md'):
            print(file)
            # get the content of the file
            content = open(file).read()
            # parse the markdown
            parsed = markdown_parser(content)
            # remove the html tags from each list element
            parsed = [BeautifulSoup(p, features="html.parser").get_text() for p in parsed]
        else:
            continue
        for p in parsed:
            print(file)
            # filename = file.replace("@@", "/")
            pass
            # add the information to the graph