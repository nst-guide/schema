import json

from jsonschema import validate as jsonvalidate
from pkg_resources import resource_filename


def validate(instance, table_name):
    schema_path = get_schema_path(table_name)
    with open(schema_path) as f:
        schema = json.load(f)
    jsonvalidate(instance=instance, schema=schema)


def get_schema_path(table_name):
    return resource_filename('nstschema', f'schemas/{table_name}.json')
