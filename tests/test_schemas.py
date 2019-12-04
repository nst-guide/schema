import json
from pathlib import Path

import pytest
from nstschema import validate

# Each folder should be named the same as a json schema file, and should contain
# test JSON cases for that schema.
# Get names of folders in tests directory
folders = [x for x in Path(__file__).parents[0].iterdir() if x.is_dir()]
# Get names of JSON schema files
schema_names = [
    x.stem
    for x in (Path(__file__) / '..' / '..' / 'schemas').resolve().iterdir()
    if x.suffix == '.json'
]
# intersect folder names with json schema file names
folders = [x for x in folders if x.name in schema_names]


# Loop over all folders
@pytest.mark.parametrize("folder", folders)
def test(folder):
    for test_json_file in folder.glob('*.json'):
        with open(test_json_file) as f:
            test_json = json.load(f)

        validate(test_json, folder.name)
