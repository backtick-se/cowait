import sys
from io import StringIO


class StreamCapture(object):
    def __init__(
        self,
        stream,
        silence: bool = False,
        callback: callable = None,
    ):
        self.stream = stream
        self.silence = silence
        self.capture = StringIO()
        self.callback = callback

    def isatty(self):
        return False

    def write(self, data):
        self.capture.write(data)

        if not self.silence:
            self.stream.write(data)

        if '\n' in data:
            self.flush(auto=True)

    def flush(self, auto: bool = False):
        if not self.silence:
            self.stream.flush()

        if callable(self.callback):
            self.callback(self.getvalue())

        self.capture = StringIO()

    def getvalue(self):
        data = self.capture.getvalue()
        return data


class StreamCapturing(object):
    def __init__(
        self,
        on_stdout: callable = None,
        on_stderr: callable = None,
        silence=False,
    ):
        self.on_stdout = on_stdout
        self.on_stderr = on_stderr
        self.silence = silence

    def __enter__(self):
        self.stdout = StreamCapture(
            stream=sys.stdout,
            callback=self.on_stdout,
            silence=self.silence,
        )
        self.stderr = StreamCapture(
            stream=sys.stderr,
            callback=self.on_stderr,
            silence=self.silence,
        )
        # capture outputs
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, *args):
        # reset outputs
        sys.stdout = self.stdout.stream
        sys.stderr = self.stderr.stream

    def __del__(self):
        del self.stdout
        del self.stderr
