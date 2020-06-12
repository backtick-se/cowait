

class ParentTask(object):
    def __init__(self, node):
        self.parent = node.parent

    @property
    def id(self) -> str:
        return self.parent.id

    async def call(self, method, args={}):
        if not self.parent.connected:
            raise RuntimeError('Not connected to parent')

        if self.parent.rpc is None:
            raise RuntimeError('Parent RPC unavailable')

        return await self.parent.rpc.call(method, args)

    def __getattr__(self, method):
        async def magic_rpc(*args, **kwargs):
            if len(args) > 0:
                raise TypeError('Positional arguments are not supported for RPC methods')
            return await self.call(method, kwargs)
        return magic_rpc
