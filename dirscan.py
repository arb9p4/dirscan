import os
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('output')
args = parser.parse_args()

BLOCK_SIZE = 65536

def hash(fd):
    file_hash = hashlib.sha256()
    try:
        with open(fd, 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)
    except:
        return ''
    return file_hash.hexdigest()

path = os.path.normpath(args.path)

with open(args.output, 'w') as fid:

    fid.write(f'index\tparent\tname\tsize\tatime\tmtime\tctime\tsha256\n')

    st = os.stat(path)
    fh = hash(path)
    fid.write(f'0\t{-1}\t{path}\t{st.st_size}\t{st.st_atime}\t{st.st_mtime}\t{st.st_ctime}\t{fh}\n')

    def scan(path, parent):
        print(path)
        index = parent
        try:
            for fd in os.scandir(path):
                index += 1
                st = fd.stat()
                fh = hash(fd)
                fid.write(f'{index}\t{parent}\t{fd.name}\t{st.st_size}\t{st.st_atime}\t{st.st_mtime}\t{st.st_ctime}\t{fh}\n')
                if fd.is_dir():
                    index = scan(fd.path, index)
        except:
            pass
        return index

    scan(path, 0)

