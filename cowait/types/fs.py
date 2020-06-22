from cowait.storage import StorageBackends, FileFormats
from .type import Type
from .mapping import TypeAlias


@TypeAlias(*FileFormats)
class FileType(Type):
    name: str = 'File'

    def validate(self, value: any, name: str) -> None:
        if not isinstance(value, dict):
            raise TypeError(f'Expected {name} to be dict file representation')

        if 'path' not in value:
            raise TypeError(f'File {name} has no path')

        if 'fs' not in value:
            raise TypeError(f'File {name} has no path')

    def serialize(self, file) -> dict:
        return {
            'path': file.path,
            'fs': file.fs.to_json(),
        }

    def deserialize(self, value: dict):
        fs = StorageBackends.from_json(value['fs'])
        return fs.open(value['path'])
