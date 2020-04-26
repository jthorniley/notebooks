#!/usr/bin/env python

import os
from pathlib import Path
import tempfile
import subprocess
import shutil


def root_path():
    p = Path(os.path.dirname(os.path.realpath(__file__)))
    if not p.exists():
        raise RuntimeError('Unable to find root path')
    return p


def docs_path():
    docs = root_path() / 'docs'
    if not docs.exists():
        raise RuntimeError('Docs folder not found')
    return docs


def exec(cmd, cwd):
    cmd = cmd.split()
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f'Command {cmd} failed')


def main():
    print(f'Rebuilding docs')
    exec('rm -rf _build', docs_path().as_posix())
    exec('poetry run bash convert.sh', root_path().as_posix())
    tmp_dir = tempfile.TemporaryDirectory()
    print(f'Building in {tmp_dir.name}')
    exec(f'git clone git@github.com:jthorniley/notebooks.git .', tmp_dir.name)
    exec(f'git checkout gh-pages', tmp_dir.name)
    exec(f'git rm *', tmp_dir.name)
    shutil.copytree(docs_path() / '_build' / 'html',
                    tmp_dir.name,
                    dirs_exist_ok=True)
    exec(f'git add *', tmp_dir.name)
    exec(f'git commit -m PublishPages', tmp_dir.name)
    exec(f'git push', tmp_dir.name)


if __name__ == '__main__':
    main()
