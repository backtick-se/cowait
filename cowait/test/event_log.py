import re


class EventLog(list):
    """
    EventList is used to organize and query task event output.
    """

    def collect(self, stream: iter):
        """ Collects all the output events from a task. """
        for msg in stream:
            self.append(msg)

    def match(self, **search: dict) -> list:
        """
        Returns all events with fields matching the provided regex dict.
        Each value in the search dict is matched against the event value at the corresponding key.
        """
        return EventLog([d for d in self if dict_match(search, d)])

    def match_one(self, **search: dict) -> dict:
        """
        Returns the first event fields matching the provided regex dict.
        Each value in the search dict is matched against the event value at the corresponding key.
        """
        results = self.match(**search)
        if len(results) == 0:
            return None
        return results[0]

    def count(self, **search: dict) -> int:
        matches = 0
        for item in self:
            if dict_match(search, item):
                matches += 1
        return matches

    def has(self, **search: dict) -> bool:
        """
        Checks if a event of a certain type has been captured with fields matching the provided
        regex dict. Each value in the search dict is matched against the event value at the
        corresponding key.
        """
        return self.count(**search) > 0

    def extract(self, key: str) -> list:
        return [msg[key] for msg in self if key in msg]

    def unique(self, key) -> set:
        return set(self.extract(key))


def dict_match(search: dict, item: dict) -> bool:
    for key, regex in search.items():
        if regex is None:
            continue
        if key not in item:
            return False
        if re.search(regex, item[key]) is None:
            return False
    return True
