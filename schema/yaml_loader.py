import yaml

from schema import rx


def load_file(file_path, schema_path=None):
    with open(file_path) as f:
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
