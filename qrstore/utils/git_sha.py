from __future__ import absolute_import

import os.path

__all__ = 'GitSha'

def GitSha():
    path = os.path.curdir
    deployment_path = os.path.join(path, 'git_sha.txt')

    if os.path.exists(deployment_path):
        with open(deployment_path) as fh:
            return fh.read().strip()

    head_path = os.path.join(path, '.git', 'HEAD')

    with open(head_path, 'r') as fp:
        head = fp.read().strip()

    if head.startswith('ref: '):
        head = head[5:]
        revision_file = os.path.join(
            path, '.git', *head.split('/')
        )
    else:
        return head

    if not os.path.exists(revision_file):
        # Check for Raven .git/packed-refs' file since a `git gc` may have run
        # https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
        packed_file = os.path.join(path, '.git', 'packed-refs')
        if os.path.exists(packed_file):
            with open(packed_file) as fh:
                for line in fh:
                    line = line.rstrip()
                    if line and line[:1] not in ('#', '^'):
                        try:
                            revision, ref = line.split(' ', 1)
                        except ValueError:
                            continue
                        if ref == head:
                            return revision

    with open(revision_file) as fh:
        return fh.read().strip()