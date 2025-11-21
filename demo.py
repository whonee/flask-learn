import tempfile
import os

fd, path = tempfile.mkstemp()


print(fd, path)

with open(fd, 'w') as f:
    print(f.fileno())

os.unlink(path)
