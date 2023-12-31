from thefuzz import fuzz, process
import json
import pickle
import sys

with open("../state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

G = pickle.load(open(f'../state/{repo_id}/state_0.pkl', 'rb'))

class StringSearch():

    def __init__(self, G=G) -> None:
        self.listofstrings = [n[0] for n in G.nodes(data=True)]
        self.listofclasses = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'class']
        self.listofmethods = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'method']
        self.listoffunctions = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'function']
        self.dispatch = {
            'all': self.listofstrings,
            'class': self.listofclasses,
            'class-method': self.listofmethods,
            'function': self.listoffunctions,
        }
        self.types = ['all', 'class', 'class-method', 'function']

    def best_type(self, string):
        return process.extractOne(string, self.types, scorer=fuzz.token_sort_ratio)[0]

    def add_strings(self, type='all'):
        type = self.best_type(type)
        self.listofstrings.extend(self.dispatch[type])

    def search(self, string, type='all'):
        type = self.best_type(type)
        return process.extract(string, self.dispatch[type], scorer=fuzz.token_sort_ratio)
    
    def search_one(self, string, type='all'):
        type = self.best_type(type)
        return process.extractOne(string, self.dispatch[type], scorer=fuzz.token_sort_ratio)
    
    def search_best(self, string, type='all'):
        type = self.best_type(type)
        return process.extractBests(string, self.dispatch[type], scorer=fuzz.token_sort_ratio)
    
    def search_all(self, string, type='all'):
        type = self.best_type(type)
        return process.extractAll(string, self.dispatch[type], scorer=fuzz.token_sort_ratio)
    
    def get_one_from_each(self, string):
        return {
            'all': self.search_one(string, type='all'),
            'class': self.search_one(string, type='class'),
            'class-method': self.search_one(string, type='class-method'),
            'function': self.search_one(string, type='function'),
        }
    
    def match_type_to_string(self, string):
        return process.extractOne(string, self.types, scorer=fuzz.token_sort_ratio)[0]