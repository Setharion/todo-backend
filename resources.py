import json
from typing import List
import os

def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            entry.add_entry(cls.from_json(sub_entry))
        return entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            file = json.load(f)
        return cls.from_json(file)

class EntryManager:
    def __init__(self, data_path: str):
        self.entries = []
        self.data_path = data_path
        self.entries: List[Entry]

    def save(self):
        for item in self.entries:
            item.save(self.data_path)

    def load(self):
        for item in os.listdir(self.data_path):
            if item.endswith(".json"):
                entry = Entry.load(os.path.join(self.data_path, item))
                self.entries.append(entry)