import json

from jsonschema import validate as jsonvalidate
from pkg_resources import resource_filename


def validate(instance, schema_name):
    """Validate JSON against schema

    Args:
        - instance (dict): JSON instance
        - schema_name (str): name of schema to validate against
    """
    schema_path = get_schema_path(schema_name.lower())
    with open(schema_path) as f:
        schema = json.load(f)
    jsonvalidate(instance=instance, schema=schema)


def get_schema_path(schema_name):
    return resource_filename('nstschema', f'schemas/{schema_name}.json')
