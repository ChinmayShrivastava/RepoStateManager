import click
import uuid
import os
import json
from git import Repo
import logging

def clone_repo(repo_url, repo_name, directory):

    # assert all the three arguments are not empty
    assert repo_url is not None
    assert repo_name is not None
    assert directory is not None

    # Clone the repository
    Repo.clone_from(repo_url, directory+'/data/'+repo_name)

    # click.echo(click.style(f'Repository {repo_name} cloned successfully with ID {repo_id}.', fg='green'))
    logging.info(f'Repository {repo_name} cloned successfully.')