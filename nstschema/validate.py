import json

import jsonschema
from pkg_resources import resource_filename

schema_dir = resource_filename('nstschema', 'schemas')
resolver = jsonschema.RefResolver('file://' + schema_dir + '/', None)


def validate(instance, schema_name):
    """Validate JSON against schema

    Args:
        - instance (dict): JSON instance
        - schema_name (str): name of schema to validate against
    """
    schema_path = get_schema_path(schema_name.lower())
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(
        instance=instance,
        schema=schema,
        resolver=resolver,
        format_checker=jsonschema.draft7_format_checker)


def get_schema_path(schema_name):
    return resource_filename('nstschema', f'schemas/{schema_name}.json')
