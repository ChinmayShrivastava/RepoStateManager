import click
import uuid
import os
import json
from git import Repo

@click.command()
@click.argument('repo_url')
@click.argument('repo_name')
def clone_repo(repo_url, repo_name):
    # Generate a UUID
    repo_id = str(uuid.uuid4())

    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Clone the repository
    Repo.clone_from(repo_url, f'data/{repo_id}')

    # update the repo map that maps the name to the id, the repo map is stored in a json file
    if os.path.exists('repo_map.json'):
        with open('repo_map.json') as f:
            try:
                repo_map = json.load(f)
            except json.decoder.JSONDecodeError:
                repo_map = {}
    else:
        repo_map = {}

    repo_map[repo_name] = repo_id

    # Save the dictionary into a JSON file
    with open('repo_map.json', 'w') as f:
        json.dump(repo_map, f)

    click.echo(click.style(f'Repository {repo_name} cloned successfully with ID {repo_id}.', fg='green'))

if __name__ == '__main__':
    clone_repo()