import docker

# shim that allows passing dockerfiles as a string together with a context path.
# this removes the need to write temporary files!
# source: https://github.com/docker/docker-py/issues/2105
docker.api.build.process_dockerfile = lambda dockerfile, path: ('Dockerfile', dockerfile)


class Dockerfile(object):
    """ Simple tool for creating dockerfiles """

    def __init__(self, base):
        self.lines = [f'FROM {base}']

    def copy(self, src, dst):
        self.lines.append(f'COPY {src} {dst}')

    def run(self, cmd):
        self.lines.append(f'RUN {cmd}')

    def env(self, key: str, value: str):
        self.lines.append(f'ENV {key}={value}')

    def workdir(self, path):
        self.lines.append(f'WORKDIR {path}')

    def __str__(self):
        return '\n'.join(self.lines)

    @staticmethod
    def read(path):
        with open(path, 'r') as f:
            df = Dockerfile('none')
            df.lines = f.readlines()
            return df
