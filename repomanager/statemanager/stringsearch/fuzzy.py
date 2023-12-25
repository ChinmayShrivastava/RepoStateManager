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

    def add_strings(self, listofstrings):
        self.listofstrings.extend(listofstrings)

    def search(self, string):
        return process.extract(string, self.listofstrings, scorer=fuzz.token_sort_ratio)
    
    def search_one(self, string):
        return process.extractOne(string, self.listofstrings, scorer=fuzz.token_sort_ratio)
    
    def search_best(self, string):
        return process.extractBests(string, self.listofstrings, scorer=fuzz.token_sort_ratio)
    
    def search_all(self, string):
        return process.extractAll(string, self.listofstrings, scorer=fuzz.token_sort_ratio)
    
    def search_nbest(self, string):
        return process.extractNBest(string, self.listofstrings, scorer=fuzz.token_sort_ratio)