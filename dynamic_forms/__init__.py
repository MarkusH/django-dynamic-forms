# -*- coding: utf-8 -*-
from __future__ import unicode_literals


VERSION = (0, 3, 0, 'alpha', 0)


def get_version(full=True):
    """Derives a PEP386-compliant version number from VERSION.

    Taken from django.utils.version.get_git_changeset at rev ce5e09353d
    """

    def get_git_changeset():
        """Returns a numeric identifier of the latest git changeset.

        Taken from django.utils.version.get_git_changeset at rev ce5e09353d.
        """
        import datetime
        import subprocess
        from os.path import abspath, dirname
        repo_dir = dirname(dirname(abspath(__file__)))
        git_log = subprocess.Popen(
            'git log --pretty=format:%ct --quiet -1 HEAD',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=repo_dir, universal_newlines=True)
        timestamp = git_log.communicate()[0]
        try:
            timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
        except ValueError:
            return None
        return timestamp.strftime('%Y%m%d%H%M%S')

    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if VERSION[2] == 0 else 3
    if not full:
        return '.'.join(str(x) for x in VERSION[:2])
    main = '.'.join(str(x) for x in VERSION[:parts])

    sub = ''
    if VERSION[3] == 'alpha' and VERSION[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev%s' % git_changeset

    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[VERSION[3]] + str(VERSION[4])

    return str(main + sub)
