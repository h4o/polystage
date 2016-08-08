import os

import yaml

from python.schema import rx


def load_file(file_path, schema_path=None):
    """Tries to open load the file at ./data/file_path. If it fails, tries again at ./file_path"""
    if not file_path.endswith('.yml'):
        file_path += '.yml'
    path = os.path.join('data', file_path)
    if not os.path.exists(path):
        path = file_path
    with open(path) as f:
        file = yaml.safe_load(f)
        if schema_path:
            _validate(file, schema_path)

        return file


def _validate(file, schema_path):
    with open(schema_path) as schema_file:
        schema_yaml = yaml.safe_load(schema_file)
        factory = rx.Factory()
        validator = factory.make_schema(schema_yaml)
        validator.validate(file)
