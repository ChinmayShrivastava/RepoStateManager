import click
import os

def set_directory():
    directory = None
    while True:
        # confidm wheather the user wants to clone the repo in the current working directory and print the current working directory in yellow
        click.echo(click.style(f'Current working directory is {os.getcwd()}. Do you want to clone the repository in the current working directory? (y/n)', fg='yellow'))
        # get the user input
        user_input = input()
        # if the user input is y, then set the directory to the current working directory
        if user_input == 'y':
            directory = os.getcwd()
            break
        # if the user input is n, then ask the user to enter the directory
        elif user_input == 'n':
            click.echo(click.style('Enter the directory where you want to clone the repository.', fg='yellow'))
            directory = input()
            break
        # if the user input is neither y nor n, then ask the user to enter the input again
        else:
            click.echo(click.style('Invalid input. Please enter y or n.', fg='yellow'))
    # return the directory
    return directory

def get_files_to_ignore(repo_root_dir):
    ignore = []
    # open gitignore from the root directory
    with open(repo_root_dir+'.gitignore', 'r') as f:
        _ignore = f.readlines()
    for i in _ignore:
        # if the line isn't a comment or a space or a newline
        if i[0] != '#' and i[0] != '\n' and i[0] != ' ':
            # strip the newline
            ignore.append(i.strip())
    return ignore
