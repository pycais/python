def generate_model(data):
    def parse_value(value):
        """Helper function to parse a value and return its type as a string."""
        if isinstance(value, dict):
            return parse_dict(value)
        elif isinstance(value, list):
            if value:
                # Assume all elements in the list are of the same type
                return [parse_value(value[0])]
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

    def parse_dict(d):
        """Helper function to parse a dictionary and return its type as a dictionary."""
        parsed = {'age': 'int',
                  'is_active': 'int',
                  'name': 'str',
                  'phone_numbers': ['str'],
                  'preferences': {'contact': {'email': 'int', 'sms': 'int'},
                                  'languages': ['str']}}

        for key, value in d.items():
            parsed[key] = parse_value(value)
        return parsed

    return parse_dict(data)


# Example usage
input_data = {
    "name": "Alice",
    "age": 30,
    "address": [
        {"addr": "123 Main St", "num": 231, "ee": '123'},
        {"addr": "123 Main St2", "num": 21},
        {"addr": "123 Main St3", "num": 31, "ee": 'ew'}
    ],
    "phone_numbers": ["123-456-7890", "098-765-4321"],
    "is_active": True,
    "preferences": {
        "contact": {
            "email": True,
            "sms": False
        },
        "languages": ["English", "French"]
    }
}

if __name__ == '__main__':
    from pprint import pprint

    pprint(generate_model(input_data))
