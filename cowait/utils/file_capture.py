import os
import io
import sys
from tempfile import TemporaryFile

SYS_FDS = {
    1: 'stdout',
    2: 'stderr',
}


class CallbackFile(io.TextIOWrapper):
    def __init__(self, callback: callable = None):
        super().__init__(
            TemporaryFile(buffering=0),
            encoding="utf-8",
            errors="replace",
            newline="",
            write_through=True,
        )
        self.callback = callback

    def write(self, data):
        super().write(data)
        if '\n' in data:
            self.flush()

    def getvalue(self):
        self.buffer.seek(0)
        res = self.buffer.read()
        self.buffer.seek(0)
        self.buffer.truncate()
        return res.decode('utf-8')

    def flush(self):
        if self.callback is not None:
            text = self.getvalue()
            if len(text) > 0:
                self.callback(text)
        else:
            super().flush()


class FDCapture:
    def __init__(self, targetfd: int, callback: callable = None) -> None:
        self.targetfd = targetfd
        self.targetfd_save = os.dup(targetfd)
        self.tmpfile = CallbackFile(callback)
        self._capturing = False

    def start(self) -> None:
        """Start capturing on targetfd using memorized tmpfile."""
        assert not self._capturing

        # redirect the target fd to our temporary file
        os.dup2(self.tmpfile.fileno(), self.targetfd)

        if self.targetfd in SYS_FDS:
            # for system file descriptors (stdout, stderr) we also need to replace the sys.stdout/sys.stderr streams.
            # this allows us to capture output from the local python process
            self.sysfile = getattr(sys, SYS_FDS[self.targetfd])
            setattr(sys, SYS_FDS[self.targetfd], self.tmpfile)

        self._capturing = True

    def stop(self) -> None:
        """Stop capturing, restore streams & return original capture file"""
        assert self._capturing

        # disable output redirection
        os.dup2(self.targetfd_save, self.targetfd)

        # close temporary file descriptor
        os.close(self.targetfd_save)

        if self.targetfd in SYS_FDS:
            # restore the original sys stream
            setattr(sys, SYS_FDS[self.targetfd], self.sysfile)

        self._capturing = False

    def writeorg(self, data):
        """Write to original file descriptor."""
        assert self._capturing
        os.write(self.targetfd_save, data.encode('utf-8'))

    def snap(self):
        return self.tmpfile.getvalue()

    def __del__(self):
        self.tmpfile.close()


class FDTransform(FDCapture):
    def __init__(self, targetfd: int, transformer: callable):
        def callback(data):
            self.writeorg(transformer(data))

        super().__init__(targetfd, callback)
