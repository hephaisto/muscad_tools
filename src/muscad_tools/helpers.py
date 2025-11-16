from typing import Any, Iterable

class DataTable:
    def __init__(self, fields: list[str], values: dict[Any, Iterable[float]]):
        self.data = {}
        for key, value_list in values.items():
            assert len(fields) == len(value_list)
            self.data[key] = {fields[i]: value_list[i] for i in range(len(fields))}

    def __getitem__(self, key):
        return self.data[key]
