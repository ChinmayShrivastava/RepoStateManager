from clone.clone import clone_repo
from map.map import map_repo
from ast.tree import element_tree
from states.initialize import initialize_state
from general import set_directory, get_files_to_ignore
import click
import os
import logging

DISPATCH = {
    'clone': False,
    'map': False,
    'tree': False,
    'initstate': False,
}

DEPENDENCY_DISPATCH = {
    'clone': [],
    'map': ['clone'],
    'tree': ['map'],
    'initstate': ['tree'],
}

WHICH_DIR = {
    "data": "{dir}/data/",
    "dirmap": "{dir}/dirmap.json",
    "treemap": "{dir}/treemap.json",
    "state": "{dir}/state_0.pkl",
}

def dir_dispatch(which_dir, directory):
    return WHICH_DIR[which_dir].format(dir=directory)

# define a decorator for dependency checking based on a key
def dependency_check(key, dispatch):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # check if the dependency is satisfied
            for d in DEPENDENCY_DISPATCH[key]:
                assert dispatch[d]
            # invoke the function
            func(*args, **kwargs)
        return wrapper
    return decorator

class IndexRepo:

    dispatch = DISPATCH

    def __init__(
        self,
        repo_url: str,
        repo_name: str,
        directory: str = None,
        verbose: bool = True,
        ignore: list = None,
    ):
        
        # assert the repo url is not empty
        assert len(repo_url) > 0
        # assert the repo name is not empty
        assert len(repo_name) > 0

        self.repo_url = repo_url
        self.repo_name = repo_name
        self.verbose = verbose
        # set logging
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        # set the directory
        if directory is None or len(directory) == 0:
            self.directory = set_directory()
        else:
            self.directory = directory
        # make a data directory if it doesn't exist
        os.makedirs(dir_dispatch('data', self.directory), exist_ok=True)
        # get files to ignore
        if ignore is None:
            self.ignore = get_files_to_ignore(
                dir_dispatch('data', self.directory)
            )
    
    @dependency_check('clone', dispatch)
    def _clone(self):
        if not self.dispatch['clone']:
            clone_repo(self.repo_url, self.repo_name, self.directory+'data')
            # update the dispatch
            self.dispatch['clone'] = True
        else:
            logging.info('Clone not invoked.')
        logging.info('Clone complete.')

    @dependency_check('map', dispatch)
    def _map(self):
        if not self.dispatch['map']:
            map_repo(
                dir_dispatch('dirmap', self.directory),
                dir_dispatch('data', self.directory),
                self.ignore
            )
            # update the dispatch
            self.dispatch['map'] = True
        else:
            logging.info('Map not invoked.')
        logging.info('Map complete.')

    @dependency_check('tree', dispatch)
    def _tree(self):
        if not self.dispatch['tree']:
            element_tree(
                dir_dispatch('treemap', self.directory),
                dir_dispatch('dirmap', self.directory)
            )
            # update the dispatch
            self.dispatch['tree'] = True
        else:
            logging.info('Tree not invoked.')
        logging.info('Tree complete.')

    @dependency_check('initstate', dispatch)
    def _initstate(self):
        if not self.dispatch['initstate']:
            initialize_state(
                dir_dispatch('state', self.directory),
                dir_dispatch('treemap', self.directory),
                dir_dispatch('dirmap', self.directory)
            )
            # update the dispatch
            self.dispatch['initstate'] = True
        else:
            logging.info('Initstate not invoked.')
        logging.info('Initstate complete.')

    def _index(self):
        self._clone()
        self._map()
        self._tree()
        self._initstate()

    def index(self):
        self._index()

# create a group
@click.group()
# argument takes in a public github url
@click.argument('repo_url')
# argument takes in a repo name
@click.argument('repo_name')
def index(repo_url, repo_name):
    repoindex = IndexRepo(repo_url, repo_name)
    # index repo
    repoindex.index() 