from thefuzz import fuzz, process
import json
import pickle
import sys
from typing import List, Optional

with open("state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))

class StringSearch():

    def __init__(
            self,
            listofstrings,
            listofclasses,
            listofmethods,
            listoffunctions,
            ) -> None:
        self.listofstrings = listofstrings
        self.listofclasses = listofclasses
        self.listofmethods = listofmethods
        self.listoffunctions = listoffunctions
        self.dispatch = {
            'all': self.listofstrings,
            'class': self.listofclasses,
            'class-method': self.listofmethods,
            'function': self.listoffunctions,
        }
        self.types = ['all', 'class', 'class-method', 'function']

    @classmethod
    def init_from_networkx(cls, G):
        listofstrings = [n[0] for n in G.nodes(data=True)]
        listofclasses = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'class']
        listofmethods = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'method']
        listoffunctions = [n[0] for n in G.nodes(data=True) if 'type' in n[1] and n[1]['type'] == 'function']
        return cls(
            listofstrings=listofstrings,
            listofclasses=listofclasses,
            listofmethods=listofmethods,
            listoffunctions=listoffunctions,
        )

    @classmethod
    def init_from_neo4j(cls, driver):
        listofstrings = []
        listofclasses = []
        listofmethods = []
        listoffunctions = []
        # get all nodes from teh graph
        with driver.session() as session:
            nodes = session.run(
                """
                MATCH (n) RETURN n
                """
            )
            for node in nodes:
                node = node['n']
                if 'name' in node.keys():
                    listofstrings.append(node['name'])
                if 'type' in node.keys():
                    if node['type'] == 'class':
                        listofclasses.append(node['name'])
                    if node['type'] == 'method':
                        listofmethods.append(node['name'])
                    if node['type'] == 'function':
                        listoffunctions.append(node['name'])
        return cls(
            listofstrings=listofstrings,
            listofclasses=listofclasses,
            listofmethods=listofmethods,
            listoffunctions=listoffunctions,
        )

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