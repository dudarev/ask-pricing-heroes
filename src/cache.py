import json


class Cache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        if self.cache_file.exists():
            self._cache = json.loads(self.cache_file.read_text())
        else:
            self._cache = {}

    def get(self, question):
        return self._cache.get(question)

    def set(self, question, answer):
        self._cache[question] = answer
        self.cache_file.write_text(json.dumps(self._cache, indent=2))

    def keys(self):
        return self._cache.keys()
