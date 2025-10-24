import asyncio, tempfile, os

async def main():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write("print('hello from file')")
        path = f.name
    proc = await asyncio.create_subprocess_exec('python', path,
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    print('returncode', proc.returncode)
    print('out:', out.decode())
    print('err:', err.decode())
    os.unlink(path)

asyncio.run(main())
