import asyncio

async def main():
    proc = await asyncio.create_subprocess_exec('python', '-c', "print('hello async')",
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    print('returncode', proc.returncode)
    print('out:', out.decode())
    print('err:', err.decode())

asyncio.run(main())
