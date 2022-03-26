# -*- coding:utf-8 -*-
from asyncio.windows_utils import BUFSIZE
import sys
import asyncio


class PipeAdapter(object):
    BUFFER_SIZE = 4096

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()

    async def connect(self, 
                      in_ = sys.stdin,
                      out_ = sys.stdout) -> None:
        self.loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(self.reader)
        await self.loop.connect_read_pipe(lambda: protocol, in_)

        transport, protocol = await self.loop.connect_write_pipe(asyncio.streams.FlowControlMixin, out_)
        writer = asyncio.StreamWriter(transport, protocol, reader, self.loop)

        self.reader = reader
        self.writer = writer

        return reader, writer

    async def recv(self):
        data = await self.reader.read(self.BUFFER_SIZE)
        sys.stderr.write("Recv: {}".format(data))

        return data

    async def send(self, data: bytes):
        await self.writer.write(data)


async def main():
    svc = PipeAdapter()
    await svc.connect()

    while True:
        data = await svc.recv()
        await svc.send(data)


if __name__ == '__main__':
    asyncio.run(main())
