import click
from defaults.trackers import DEFAULT_MIGRATIONS_TRACKER
import json
import os
import logging
from databases.neo4j.direct_migration import migrate as migrate_graph
from databases.vector.chroma2pinecone import migrate as migrate_vector
import pickle

# We can create the sql database to store conversations. 
# To store the indexed data itself, we don't need it as the file data can also be stored in graph itself.
# will implement the sql databe store for chats later

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
def migrate_to_database(repo_name):

    repo_id = repo_map[f'{repo_name}']
    print(repo_id)
    G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))

    # if the state/repo_id/meta/defaults/migrations.json file doesn't exist, create it
    if not os.path.exists(f'state/{repo_id}/meta/defaults/migrations.json'):
        with open(f'state/{repo_id}/meta/defaults/migrations.json', 'w') as f:
            json.dump(DEFAULT_MIGRATIONS_TRACKER, f)

    # if the state/repo_id/meta/defaults/migrations.json file exists, read it
    with open(f'state/{repo_id}/meta/defaults/migrations.json', 'r') as f:
        migrations_tracker = json.load(f)

    if not migrations_tracker['neo4j']:
        migrate_graph(repo_name, repo_id, G)
        migrations_tracker['neo4j'] = True
        with open(f'state/{repo_id}/meta/defaults/migrations.json', 'w') as f:
            json.dump(migrations_tracker, f)
        logging.info(f'neo4j migration complete for {repo_name}')

    if not migrations_tracker['vector']:
        migrate_vector(repo_name, repo_id, G, code=True)
        migrations_tracker['vector'] = True
        with open(f'state/{repo_id}/meta/defaults/migrations.json', 'w') as f:
            json.dump(migrations_tracker, f)
        logging.info(f'vector migration complete for {repo_name}')
        pass
    return

if __name__ == '__main__':
    migrate_to_database()