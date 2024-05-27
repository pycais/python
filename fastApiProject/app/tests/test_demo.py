"""
@author: cs
@version: 1.0.0
@file: test_demo.py
@time: 2024/5/23 0:40
@description: 
"""
class ModelMerger:
    def __init__(self):
        self.merged_model = {}

    def parse_value(self, value):
        """Helper function to parse a value and return its type as a string."""
        if isinstance(value, dict):
            return self.parse_dict(value)
        elif isinstance(value, list):
            if value:
                return [self.parse_value(value[0])]
            else:
                return ['Any']
        elif isinstance(value, str):
            return 'str'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, bool):
            return 'bool'
        else:
            return 'Any'

    def parse_dict(self, d):
        """Helper function to parse a dictionary and return its type as a dictionary."""
        parsed = {}
        for key, value in d.items():
            parsed[key] = self.parse_value(value)
        return parsed

    def merge_values(self, v1, v2):
        """Merge two values which could be types, lists or dictionaries."""
        if isinstance(v1, dict) and isinstance(v2, dict):
            return self.merge_dicts(v1, v2)
        elif isinstance(v1, list) and isinstance(v2, list):
            if v1 and v2:
                return [self.merge_values(v1[0], v2[0])]
            elif not v1:
                return v2
            else:
                return v1
        else:
            if v1 != v2:
                return 'Any'
            return v1

    def merge_dicts(self, d1, d2):
        """Merge two parsed dictionaries."""
        for key, value in d2.items():
            if key in d1:
                d1[key] = self.merge_values(d1[key], value)
            else:
                d1[key] = value
        return d1

    def add_dict(self, new_dict):
        """Add a new dictionary to the model and merge its structure."""
        parsed_dict = self.parse_dict(new_dict)
        self.merged_model = self.merge_dicts(self.merged_model, parsed_dict)

    def get_model(self):
        """Get the current merged model."""
        return self.merged_model

# Example usage
model_merger = ModelMerger()

input_data1 = {
    "name": "Alice",
    "age": 30,
    "address": [],
    "city": "Wonderland",
    "coordinates": {
        "latitude": 52.52,
        "longitude": 13.405
    },
    "phone_numbers": ["123-456-7890"],
    "is_active": True,
    "preferences": {
        "contact": {
            "email": True,
            "sms": False
        },
        "languages": ["English"]
    }
}

input_data2 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St", "num": 231, "ee": '123'},
        {"addr": "123 Main St2", "num": 21}
    ],
    "city": "Wonderland",
    "coordinates": {
        "latitude": 40.7128,
        "longitude": 74.0060
    },
    "phone_numbers": ["987-654-3210"],
    "is_active": False,
    "preferences": {
        "contact": {
            "email": False,
            "sms": True
        },
        "languages": ["French", "Spanish"]
    },
    "new_field": "new_value"
}



input_data1 = {
    "name": "Alice",
    "age": 30,
    "address": []
}

input_data2 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St", "num": 231, "ee": '123'},
        {"addr": "123 Main St2", "num": 21}
    ]
}
# Adding dictionaries one by one
model_merger.add_dict(input_data1)
model_merger.add_dict(input_data2)

# Getting the merged model
merged_model = model_merger.get_model()
print(merged_model)
