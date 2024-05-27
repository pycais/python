import math
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('mysql+pymysql://root:QWE&qwe..123@192.168.74.129/test')
Session = sessionmaker(bind=engine)
session = Session()


class ModelMerger:
    def __init__(self):
        self.merged_model = {}
        self.string_lengths = {}

    def parse_value(self, key, value):
        """Helper function to parse a value and return its type as a string."""
        if isinstance(value, dict):
            return self.parse_dict(value)
        elif isinstance(value, list):
            if value:
                return [self.parse_value(key, value[0])]
            else:
                return ['Any']
        elif isinstance(value, str):
            length = len(value)
            if key in self.string_lengths:
                self.string_lengths[key] = max(self.string_lengths[key], length)
            else:
                self.string_lengths[key] = length
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
            parsed[key] = self.parse_value(key, value)
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
            if v1 == 'Any':
                return v2
            elif v2 == 'Any':
                return v1
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


def next_power_of_2(x):
    """Calculate the next power of 2 greater than or equal to x."""
    return 2 ** math.ceil(math.log2(x))


def create_sqlalchemy_model(table_name, model_description, base_class, string_lengths, main_identifier, models_dict):
    """Generate a SQLAlchemy model class from a model description."""
    attributes = {'__tablename__': table_name}

    # Add a primary key 'id' to every table
    attributes['id'] = Column(Integer, primary_key=True)

    # Add a create_time field to every table
    attributes['create_time'] = Column(DateTime, default=datetime.utcnow)

    # Add the logical relationship field
    attributes[main_identifier] = Column(String(64))

    for key, value in model_description.items():
        if isinstance(value, str):
            if value == 'str':
                max_length = string_lengths.get(key, 64)
                adjusted_length = next_power_of_2(max_length)
                attributes[key] = Column(String(adjusted_length))  # Use adjusted length
            elif value == 'int':
                attributes[key] = Column(Integer)
            elif value == 'float':
                attributes[key] = Column(Float)
            elif value == 'bool':
                attributes[key] = Column(Boolean)
            else:
                attributes[key] = Column(String(64))
        elif isinstance(value, list) and value:
            nested_table_name = f"{table_name}_{key}"
            nested_model_class = create_sqlalchemy_model(nested_table_name, value[0], base_class, string_lengths,
                                                         main_identifier, models_dict)
            models_dict[nested_table_name] = nested_model_class
        elif isinstance(value, dict):
            nested_table_name = f"{table_name}_{key}"
            nested_model_class = create_sqlalchemy_model(nested_table_name, value, base_class, string_lengths,
                                                         main_identifier, models_dict)
            models_dict[nested_table_name] = nested_model_class

    model_class = type(table_name.capitalize(), (base_class,), attributes)
    models_dict[table_name] = model_class
    return model_class


def insert_data(session, model_class, data, main_identifier, main_id_value, models_dict):
    """Insert data into the corresponding SQLAlchemy model class."""
    if isinstance(data, list):
        for item in data:
            insert_data(session, model_class, item, main_identifier, main_id_value, models_dict)
        return

    if not isinstance(data, dict):
        return

    instance_data = {main_identifier: main_id_value}
    relationships_data = {}

    for key, value in data.items():
        if isinstance(value, list) or isinstance(value, dict):
            relationships_data[key] = value
        else:
            instance_data[key] = value

    instance = model_class(**instance_data)
    session.add(instance)
    session.flush()  # Ensure the instance gets an ID before inserting related data

    for key, value in relationships_data.items():
        related_table_name = f"{model_class.__tablename__}_{key}"
        related_model = models_dict[related_table_name]
        related_data = value

        if isinstance(related_data, list):
            for item in related_data:
                item[main_identifier] = main_id_value
        elif isinstance(related_data, dict):
            related_data[main_identifier] = main_id_value

        insert_data(session, related_model, related_data, main_identifier, main_id_value, models_dict)

    session.commit()


# Example usage
model_merger = ModelMerger()

input_data1 = {
    "name": "Alice",
    "age": 30,
    "address": [{"addr": "43", "ee": "ee"}]
}

input_data2 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St", "num": 231, "ee": '123'},
        {"addr": "123 Main St2", "num": 21}
    ]
}

input_data3 = {
    "name": "Bob",
    "age": 25,
    "address": [
        {"addr": "123 Main St2", "num": 2211, 'xx': 123},
        {"addr": "123 Main St2", "num": 2212, 'xx': 32},
        {"addr": "123 Main St2", "num": 2213, 'ee': 'ad'}
    ]
}

# Adding dictionaries one by one
model_merger.add_dict(input_data1)
model_merger.add_dict(input_data2)
model_merger.add_dict(input_data3)

# Getting the merged model
merged_model = model_merger.get_model()
print(merged_model)

# Main identifier for linking tables
main_identifier = 'age'

# Creating SQLAlchemy models
models_dict = {}
MainModel = create_sqlalchemy_model('main', merged_model, Base, model_merger.string_lengths, main_identifier,
                                    models_dict)
Base.metadata.create_all(engine)

# Inserting data into the created tables
insert_data(session, MainModel, input_data1, main_identifier, input_data1[main_identifier], models_dict)
insert_data(session, MainModel, input_data2, main_identifier, input_data2[main_identifier], models_dict)
insert_data(session, MainModel, input_data3, main_identifier, input_data3[main_identifier], models_dict)

# Query the database to verify data insertion
for instance in session.query(MainModel).all():
    print(instance.name, instance.age)
